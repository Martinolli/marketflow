"""
This script generates embeddings for text chunks using the OpenAI API.
It processes chunks in batches to improve efficiency and avoids re-embedding already processed chunks.

How to use:
# Make sure your OPENAI_API_KEY is set as an environment variable
# export OPENAI_API_KEY="sk-..."

python embedder.py "knowledgebase/chunked/Wyckoff_Stock_Analysis.json" "knowledgebase/embeddings/Wyckoff_Stock_Analysis.json"

"""

import os
import json
import argparse
from pathlib import Path
from openai import OpenAI
from typing import List, Dict

# Local imports
from marketflow.marketflow_logger import get_logger
from marketflow.marketflow_config_manager import create_app_config


# Use the modern OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize logger and config
# Initialize logger and config
logger = get_logger(module_name="EmbedderData")
config = create_app_config(logger=logger)


# Configuration
DEFAULT_MODEL = "text-embedding-3-small"
BATCH_SIZE = 100 # Process 100 chunks per API call

def load_chunks(path: Path) -> List[Dict]:
    """Loads chunks from a JSON file."""
    logger.info(f"Loading chunks from {path}")
    if not path.exists():
        raise FileNotFoundError(f"Chunks file {path} does not exist.")
    print(f"📄 Loading chunks from {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    logger.info(f"Loaded {len(chunks)} chunks from {path}")
    print(f"📄 Loaded {len(chunks)} chunks from {path}")

def embed_batch(batch_texts: List[str], model: str) -> List[List[float]]:
    """Embeds a batch of texts using the OpenAI API."""
    try:
        response = client.embeddings.create(
            model=model,
            input=batch_texts
        )
        return [item.embedding for item in response.data]
    except Exception as e:
        print(f"⚠️ Error embedding batch: {e}")
        # In a production system, you might want to retry or handle this more gracefully
        return [None] * len(batch_texts)

def main():
    parser = argparse.ArgumentParser(description="Generate embeddings for text chunks.")
    parser.add_argument("input_path", type=Path, help="Path to the chunked JSON file.")
    parser.add_argument("output_path", type=Path, help="Path to save the embedded JSON file.")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL, help="The embedding model to use.")
    args = parser.parse_args()

    print("📦 Loading chunks...")
    chunks_to_embed = load_chunks(args.input_path)
    logger.info(f"Loaded {len(chunks_to_embed)} chunks to embed.")
    
    # --- Efficiency Improvement: Avoid Re-embedding ---
    existing_embeddings = {}
    if args.output_path.exists():
        print("📄 Found existing embeddings file. Loading to avoid re-computation.")
        logger.info(f"Loading existing embeddings from {args.output_path}")
        with open(args.output_path, "r", encoding="utf-8") as f:
            # Create a dictionary of existing embeddings for quick lookup
            existing_data = json.load(f)
            for item in existing_data:
                existing_embeddings[item["chunk_id"]] = item
        print(f"📄 Loaded {len(existing_embeddings)} existing embeddings.")

    # Filter out chunks that are already embedded
    unprocessed_chunks = [
        chunk for chunk in chunks_to_embed if chunk["chunk_id"] not in existing_embeddings
    ]
    
    if not unprocessed_chunks:
        print("✅ All chunks are already embedded. Nothing to do.")
        return
        
    print(f"🔍 Found {len(unprocessed_chunks)} new chunks to embed.")
    logger.info(f"Found {len(unprocessed_chunks)} new chunks to embed.")

    # --- Performance Improvement: Batch Processing ---
    embedded_chunks = list(existing_embeddings.values()) # Start with the ones we already have
    print(f"💾 Embedding {len(unprocessed_chunks)} chunks in batches of {BATCH_SIZE}...")
    
    for i in range(0, len(unprocessed_chunks), BATCH_SIZE):
        batch = unprocessed_chunks[i:i + BATCH_SIZE]
        batch_texts = [chunk["text"] for chunk in batch]
        
        current_batch_num = (i // BATCH_SIZE) + 1
        total_batches = (len(unprocessed_chunks) + BATCH_SIZE - 1) // BATCH_SIZE
        print(f"⚡ Embedding batch {current_batch_num}/{total_batches}...")
        logger.info(f"Embedding batch {current_batch_num}/{total_batches}...")
        

        embeddings = embed_batch(batch_texts, args.model)

        for chunk, emb in zip(batch, embeddings):
            if emb:
                chunk["embedding"] = emb
                embedded_chunks.append(chunk)
            else:
                logger.warning(f"Failed to embed chunk {chunk['chunk_id']}. It will be skipped.")

    print(f"💾 Saving {len(embedded_chunks)} total embedded chunks to {args.output_path}")
    logger.info(f"Saving {len(embedded_chunks)} total embedded chunks to {args.output_path}")
    print(f"💾 Saving to {args.output_path}")
    args.output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output_path, "w", encoding="utf-8") as f:
        json.dump(embedded_chunks, f, ensure_ascii=False, indent=2)

    print("✅ Embedding complete.")
    logger.info("Embedding process completed successfully.")

if __name__ == "__main__":
    main()