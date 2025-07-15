"""
This script generates embeddings for text chunks using the OpenAI API
and stores them in a ChromaDB persistent vector database (SQLite).
It avoids re-embedding and re-uploading already-processed chunks.

USAGE:
    python embedder_vector_db.py \
        knowledgebase/chunked/Wyckoff_Stock_Analysis.json \
        knowledgebase/embeddings/Wyckoff_Stock_Analysis.json \
        --collection wyckoff_docs

Requirements:
    pip install chromadb openai

Set your OpenAI API key with:
    export OPENAI_API_KEY="sk-..."
"""

import os
import json
import argparse
from pathlib import Path
from typing import List, Dict
import chromadb
from openai import OpenAI
import numpy as np

from marketflow.marketflow_logger import get_logger
from marketflow.marketflow_config_manager import create_app_config

# --- Config ---
DEFAULT_MODEL = "text-embedding-3-small"
BATCH_SIZE = 100
CHROMA_PERSIST_PATH = Path("knowledgebase/vectordb")
DEFAULT_COLLECTION = "wyckoff_docs"

# --- Initialize ---
logger = get_logger(module_name="EmbedderVectorDBData")
config = create_app_config(logger=logger)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_chunks(path: Path) -> List[Dict]:
    """Load list of chunks from JSON."""
    logger.info(f"Loading chunks from {path}")
    with open(path, "r", encoding="utf-8") as f:
        chunks = json.load(f)
    logger.info(f"Loaded {len(chunks)} chunks from {path}")
    return chunks

def embed_batch(batch_texts: List[str], model: str) -> List[List[float]]:
    """Embed a batch of texts with OpenAI."""
    logger.info(f"Embedding batch of {len(batch_texts)} texts with model '{model}'")
    try:
        response = client.embeddings.create(model=model, input=batch_texts)
        logger.info("Successfully embedded batch")
        return [item.embedding for item in response.data]
    except Exception as e:
        logger.error(f"Error embedding batch: {e}")
        return [None] * len(batch_texts)

def main():
    parser = argparse.ArgumentParser(description="Embed chunks and store them in ChromaDB.")
    parser.add_argument("chunk_path", type=Path, help="Path to the chunked JSON file.")
    parser.add_argument("embedding_path", type=Path, help="Path to save the full embeddings JSON file.")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL, help="OpenAI embedding model to use.")
    parser.add_argument("--collection", type=str, default=DEFAULT_COLLECTION, help="ChromaDB collection name.")
    args = parser.parse_args()

    logger.info(f"Initializing ChromaDB at {CHROMA_PERSIST_PATH}")
    chroma_client = chromadb.PersistentClient(path=str(CHROMA_PERSIST_PATH))
    collection = chroma_client.get_or_create_collection(name=args.collection)

    # --- Load Chunks & Check Already Indexed IDs ---
    all_chunks = load_chunks(args.chunk_path)
    all_ids = [chunk['chunk_id'] for chunk in all_chunks]
    existing_ids = set(collection.get(ids=all_ids).get('ids', []))

    logger.info(f"{len(existing_ids)} chunks already present in vector DB.")
    unprocessed_chunks = [chunk for chunk in all_chunks if chunk['chunk_id'] not in existing_ids]
    if not unprocessed_chunks:
        logger.info("All chunks already present in DB. Nothing to embed.")
        print("✅ All chunks are already in the database. Nothing to do.")
        # Still update the master JSON backup for full mirror
        # (in case any records were deleted manually from DB)
    else:
        logger.info(f"Embedding and adding {len(unprocessed_chunks)} new chunks.")
        for i in range(0, len(unprocessed_chunks), BATCH_SIZE):
            batch = unprocessed_chunks[i:i+BATCH_SIZE]
            batch_texts = [c["text"] for c in batch]
            logger.info(f"Embedding batch {i//BATCH_SIZE+1}/{(len(unprocessed_chunks)+BATCH_SIZE-1)//BATCH_SIZE}")
            embeddings = embed_batch(batch_texts, args.model)
            # Only keep successes
            valid = [idx for idx, emb in enumerate(embeddings) if emb is not None]
            if not valid:
                logger.warning(f"Batch {i//BATCH_SIZE+1} failed completely. Skipping.")
                continue
            metadatas=[
                {**batch[j].get('metadata', {}), 'source': batch[j].get('source', 'unknown')}
                for j in valid
            ]
            collection.add(
                ids=[batch[j]['chunk_id'] for j in valid],
                embeddings=[embeddings[j] for j in valid],
                documents=[batch[j]['text'] for j in valid],
                metadatas=metadatas
            )

            logger.info(f"Added {len(valid)} chunks to ChromaDB.")

    # --- Update/Write Master Embedding JSON (Full Export) ---
    logger.info("Exporting full ChromaDB collection to JSON.")
    all_db_records = collection.get(include=["metadatas", "documents", "embeddings"])
    export_records = []
    for i, chunk_id in enumerate(all_db_records['ids']):
        emb = all_db_records['embeddings'][i]
        try:
            emb = emb.tolist()
        except AttributeError:
            pass  # Already a list
        record = {
            "chunk_id": chunk_id,
            "text": all_db_records['documents'][i],
            "embedding": emb
        }
        metadata = all_db_records['metadatas'][i] or {}
        # Keep metadata, and try to include 'source'
        if 'source' in metadata:
            record['source'] = metadata['source']
        else:
            # Attempt to parse source from chunk_id pattern
            if "_" in chunk_id and chunk_id.rsplit("_", 1)[-1].isdigit():
                record['source'] = chunk_id.rsplit('_', 1)[0]
            else:
                record['source'] = "unknown"
        # Always include the metadata field
        record['metadata'] = metadata
        export_records.append(record)

    args.embedding_path.parent.mkdir(parents=True, exist_ok=True)
    with open(args.embedding_path, "w", encoding="utf-8") as f:
        json.dump(export_records, f, ensure_ascii=False, indent=2)
    logger.info(f"Embedding and vector DB sync complete. Exported {len(export_records)} records.")

    print("✅ Embedding and vector DB sync complete.")

if __name__ == "__main__":
    main()
