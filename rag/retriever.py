"""
This module provides functionality to retrieve relevant chunks of text from a vector database (ChromaDB) or from JSON files containing pre-computed embeddings.

It supports:
- Retrieving top-k chunks based on a query using cosine similarity

How to use:
python rag/retriever.py "Describe the phases of accumulation?" --top_k 10 --source chroma

"""

import os
import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Optional
from functools import lru_cache
from tenacity import retry, stop_after_attempt, wait_exponential
import argparse

import openai
import chromadb

from marketflow.marketflow_logger import get_logger
from marketflow.marketflow_config_manager import create_app_config

DEFAULT_MODEL = "text-embedding-3-small"
CHROMA_PERSIST_PATH = "knowledgebase/vectordb"
DEFAULT_COLLECTION = "wyckoff_docs"
DEFAULT_EMBEDDING_DIR = Path("knowledgebase/embeddings")

logger = get_logger(module_name="Retriever")
config_manager = create_app_config(logger=logger)
openai.api_key = os.getenv("OPENAI_API_KEY")

@lru_cache(maxsize=100)
def cached_embed_query(text: str, model: str = DEFAULT_MODEL) -> Optional[np.ndarray]:
    return embed_query(text, model)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def embed_query(text: str, model: str = DEFAULT_MODEL) -> Optional[np.ndarray]:
    try:
        response = openai.embeddings.create(model=model, input=text)
        return np.array(response.data[0].embedding)
    except Exception as e:
        logger.error(f"Error embedding query: {e}")
        raise

def chroma_retrieve_top_chunks(query: str, top_k: int = 5, model: str = DEFAULT_MODEL, collection_name: str = DEFAULT_COLLECTION):
    chroma_client = chromadb.PersistentClient(path=CHROMA_PERSIST_PATH)
    collection = chroma_client.get_or_create_collection(name=collection_name)

    query_embedding = embed_query(query, model)
    if query_embedding is None:
        logger.warning("Query embedding failed.")
        return []

    logger.info("Querying ChromaDB for top chunks...")
    result = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k,
        include=["documents", "embeddings", "metadatas", "distances"]
    )

    docs = result["documents"][0]
    scores = result["distances"][0]  # L2 distances: lower is better
    metadatas = result["metadatas"][0]
    embeddings = result["embeddings"][0]

    # Optionally convert L2 distance to a similarity score
    top_chunks = []
    for doc, score, meta, emb in zip(docs, scores, metadatas, embeddings):
        top_chunks.append({
            "distance": score,
            "text": doc,
            "metadata": meta,
            "embedding": emb
        })
        logger.info(f"Chunk (distance={score:.4f}): {meta}, {doc[:100]}...")

    return top_chunks

def load_all_embeddings(embedding_dir: Path = DEFAULT_EMBEDDING_DIR) -> List[Dict[str, Any]]:
    all_embeddings = []
    for embedding_file in embedding_dir.glob("*.json"):
        with open(embedding_file, "r", encoding="utf-8") as f:
            embeddings = json.load(f)
            all_embeddings.extend(embeddings)
    return all_embeddings

def json_retrieve_top_chunks(query: str, top_k: int = 5, embedding_dir: Path = DEFAULT_EMBEDDING_DIR, model: str = DEFAULT_MODEL):
    chunks = load_all_embeddings(embedding_dir)
    query_embedding = cached_embed_query(query, model)
    if query_embedding is None:
        logger.warning("Query embedding failed. Returning empty result.")
        return []

    chunk_embeddings = np.array([np.array(chunk["embedding"]) for chunk in chunks])
    sims = np.dot(chunk_embeddings, query_embedding) / (
        np.linalg.norm(chunk_embeddings, axis=1) * np.linalg.norm(query_embedding) + 1e-8
    )
    scored = sorted(zip(sims, chunks), reverse=True, key=lambda x: x[0])
    top_chunks = []
    for score, chunk in scored[:top_k]:
        chunk['score'] = float(score)
        logger.info(f"Chunk (score={score:.4f}): {chunk.get('metadata', {})}, {chunk['text'][:100]}...")
        top_chunks.append(chunk)
    return top_chunks

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Retrieve top-k relevant chunks from ChromaDB or JSON embeddings.")
    parser.add_argument("query", type=str, help="Query to search for.")
    parser.add_argument("--top_k", type=int, default=5, help="Number of top chunks to return.")
    parser.add_argument("--source", type=str, choices=["chroma", "json"], default="chroma", help="Source of embeddings to query.")
    parser.add_argument("--collection", type=str, default=DEFAULT_COLLECTION, help="ChromaDB collection name.")
    args = parser.parse_args()

    if args.source == "chroma":
        results = chroma_retrieve_top_chunks(args.query, args.top_k, collection_name=args.collection)
    else:
        results = json_retrieve_top_chunks(args.query, args.top_k)

    for i, chunk in enumerate(results):
        print(f"\n--- Chunk {i+1} ---")
        meta = chunk.get("metadata", {})
        print(f"Source: {meta.get('source', '?')} | Page: {meta.get('page', '?')}")
        print(f"Distance: {chunk['distance']:.4f}")
        print(chunk["text"][:500] + "...")
