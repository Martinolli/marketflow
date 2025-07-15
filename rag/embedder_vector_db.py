"""
This module generates embeddings for text chunks using the OpenAI API and stores them in a ChromaDB vector database.
It processes chunks in batches to improve efficiency and avoids re-embedding already processed chunks.

How to use:
1 - Chunk the document if it's new or has been updated:
python chunker.py "knowledgebase/sources/Wyckoff_Stock_Analysis.pdf" "knowledgebase/chunked/Wyckoff_Stock_Analysis.json"

2 - Embed the chunks and store them in the vector database:
# Make sure your OPENAI_API_KEY is set
# export OPENAI_API_KEY="sk-..."

python embedder_vectordb.py "knowledgebase/chunked/Wyckoff_Stock_Analysis.json" "knowledgebase/embeddings/Wyckoff_Stock_Analysis.json"

"""

import os
import json
import argparse
import chromadb
from pathlib import Path
from openai import OpenAI
from typing import List, Dict

# Local imports
from marketflow.marketflow_logger import get_logger
from marketflow.marketflow_config_manager import create_app_config

# Use the modern OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Initialize logger and config
logger = get_logger(module_name="EmbedderVectorDBData")
config = create_app_config(logger=logger)


# --- Configuration ---
DEFAULT_MODEL = "text-embedding-3-small"
BATCH_SIZE = 100  # Process 100 chunks per API call
CHROMA_PERSIST_PATH = Path("knowledgebase/vectordb")
CHROMA_COLLECTION_NAME = "wyckoff_docs"

def load_chunks(path: Path) -> List[Dict]:
    """Loads chunks from a JSON file."""
    logger.info(f"Loading chunks from {path}")
    with open(path, "r", encoding="utf-8") as f:
        chunks = json.load(f)
    logger.info(f"Loaded {len(chunks)} chunks from {path}")
    return chunks

def embed_batch(batch_texts: List[str], model: str) -> List[List[float]]:
    """Embeds a batch of texts using the OpenAI API."""
    logger.info(f"Embedding batch of {len(batch_texts)} texts with model '{model}'")
    try:
        response = client.embeddings.create(model=model, input=batch_texts)
        logger.info("Successfully embedded batch")
        return [item.embedding for item in response.data]
    except Exception as e:
        logger.error(f"Error embedding batch: {e}")
        print(f"⚠️ Error embedding batch: {e}")
        return [None] * len(batch_texts)

def main():
    logger.info("Starting embedding and ChromaDB loading process.")
    parser = argparse.ArgumentParser(description="Generate embeddings and load them into ChromaDB.")
    parser.add_argument("chunk_path", type=Path, help="Path to the chunked JSON file.")
    parser.add_argument("embedding_path", type=Path, help="Path to save the master embeddings JSON file.")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL, help="The embedding model to use.")
    args = parser.parse_args()

    # --- 1. Initialize ChromaDB Client ---
    logger.info(f"Initializing ChromaDB client at '{CHROMA_PERSIST_PATH}'")
    print(f"⚡ Initializing ChromaDB client at '{CHROMA_PERSIST_PATH}'")
    chroma_client = chromadb.PersistentClient(path=str(CHROMA_PERSIST_PATH))
    collection = chroma_client.get_or_create_collection(name=CHROMA_COLLECTION_NAME)
    
    # --- 2. Load Source Chunks and Identify New Chunks ---
    logger.info(f"Loading source chunks from '{args.chunk_path}'")
    print(f"📦 Loading source chunks from '{args.chunk_path}'...")
    all_source_chunks = load_chunks(args.chunk_path)
    all_source_ids = [chunk['chunk_id'] for chunk in all_source_chunks]

    # Check which IDs are already in the database
    existing_ids = set(collection.get(ids=all_source_ids).get('ids', []))
    logger.info(f"Found {len(existing_ids)} chunks already in the vector database.")
    print(f"🔍 Found {len(existing_ids)} chunks already in the vector database.")

    # Determine which chunks are new
    unprocessed_chunks = [chunk for chunk in all_source_chunks if chunk['chunk_id'] not in existing_ids]

    if not unprocessed_chunks:
        logger.info("All chunks are already in the database. Nothing to do.")
        print("✅ All chunks are already in the database. Nothing to do.")
        return
    
    logger.info(f"Found {len(unprocessed_chunks)} new chunks to process and add.")
    print(f"✨ Found {len(unprocessed_chunks)} new chunks to process and add.")
    
    # --- 3. Process and Add New Chunks in Batches ---
    for i in range(0, len(unprocessed_chunks), BATCH_SIZE):
        batch = unprocessed_chunks[i:i + BATCH_SIZE]
        
        batch_texts = [chunk["text"] for chunk in batch]
        
        current_batch_num = (i // BATCH_SIZE) + 1
        total_batches = (len(unprocessed_chunks) + BATCH_SIZE - 1) // BATCH_SIZE
        logger.info(f"Embedding batch {current_batch_num}/{total_batches}")
        print(f"⚡ Embedding batch {current_batch_num}/{total_batches}...")

        # Get embeddings from OpenAI
        batch_embeddings = embed_batch(batch_texts, args.model)
        
        # Prepare data for ChromaDB
        ids_to_add = [chunk['chunk_id'] for chunk in batch]
        documents_to_add = [chunk['text'] for chunk in batch]
        metadatas_to_add = [chunk.get('metadata', {}) for chunk in batch]
        
        # Filter out any failed embeddings
        valid_indices = [idx for idx, emb in enumerate(batch_embeddings) if emb is not None]
        
        if not valid_indices:
            failed_chunk_ids = [chunk['chunk_id'] for chunk in batch]
            logger.warning(f"Batch {current_batch_num} failed completely. Skipping. Failed chunk IDs: {failed_chunk_ids}")
            print(f"⚠️ Batch {current_batch_num} failed completely. Skipping. Failed chunk IDs: {failed_chunk_ids}")
            continue
            
        # Add the successfully embedded data to ChromaDB
        collection.add(
            ids=[ids_to_add[i] for i in valid_indices],
            embeddings=[batch_embeddings[i] for i in valid_indices],
            documents=[documents_to_add[i] for i in valid_indices],
            metadatas=[metadatas_to_add[i] for i in valid_indices]
        )
        logger.info(f"Added {len(valid_indices)} chunks to ChromaDB collection '{CHROMA_COLLECTION_NAME}'.")
        print(f"💾 Added {len(valid_indices)} chunks to ChromaDB collection '{CHROMA_COLLECTION_NAME}'.")

    # --- 4. Update the Master JSON Backup File ---
    logger.info(f"Updating the master embeddings JSON file at '{args.embedding_path}'")
    print(f"🔄 Updating the master embeddings JSON file at '{args.embedding_path}'...")
    # Get all records from Chroma to ensure the JSON is a perfect mirror
    all_db_records = collection.get(include=["metadatas", "documents", "embeddings"])

    # Reconstruct the format of your original embeddings file
    records_to_save = []
    for i, chunk_id in enumerate(all_db_records['ids']):
        record = {
            "chunk_id": chunk_id,
            "text": all_db_records['documents'][i],
            "embedding": all_db_records['embeddings'][i]
        }
        
        # Access 'source' directly from the metadata in Chroma, if available
        metadata = all_db_records['metadatas'][i]
        if metadata is not None and 'source' in metadata:
            record["source"] = metadata['source']
            # If 'source' is not in Chroma's metadata, try to extract it from the chunk_id.
            # Assumes chunk_id format: "<source>_<number>", e.g., "anna_coulling_vpa_0"
            if "_" in chunk_id and chunk_id.rsplit("_", 1)[-1].isdigit():
                source = chunk_id.rsplit('_', 1)[0]
                record["source"] = source
                logger.warning(f"Source not found in metadata for chunk_id: {chunk_id}. Extracted from chunk_id: {source}")
            else:
                record["source"] = "unknown"
                logger.warning(f"Source could not be extracted from chunk_id: {chunk_id}. Set as 'unknown'.")
            logger.warning(f"Source not found in metadata for chunk_id: {chunk_id}. Extracted from chunk_id: {source}")
        
    if not args.embedding_path.parent.exists():
        args.embedding_path.parent.mkdir(parents=True, exist_ok=True)
    with open(args.embedding_path, "w", encoding="utf-8") as f:
        json.dump(records_to_save, f, ensure_ascii=False, indent=2)
        records_to_save.append(record)

    args.embedding_path.parent.mkdir(parents=True, exist_ok=True)
    with open(args.embedding_path, "w", encoding="utf-8") as f:
        json.dump(records_to_save, f, ensure_ascii=False, indent=2)


    logger.info("Embedding and database loading complete.")
    print("✅ Embedding and database loading complete.")

if __name__ == "__main__":
    main()