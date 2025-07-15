"""
Query your vector database using OpenAI embeddings and ChromaDB.

How to use:
1. Make sure your OPENAI_API_KEY is set as an environment variable:
   export OPENAI_API_KEY="sk-..."

   python query_vectordb.py "what are the three fundamental Wyckoff laws?" -k 3 --model text-embedding-3-small

You can specify the embedding model with the --model argument (default: text-embedding-3-small).
"""

import argparse
import chromadb
import os
from openai import OpenAI

# Local imports
from marketflow.marketflow_logger import get_logger
from marketflow.marketflow_config_manager import create_app_config

# Initialize clients
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
chroma_client = chromadb.PersistentClient(path="knowledgebase/vectordb")
collection = chroma_client.get_collection(name="wyckoff_docs")


# Initialize logger and config
logger = get_logger(module_name="QueryVectorDBData")
config = create_app_config(logger=logger)

# Configuration
DEFAULT_MODEL = "text-embedding-3-small"

def main():
    parser = argparse.ArgumentParser(description="Query your vector database.")
    parser.add_argument("query", type=str, help="The question to ask the knowledge base.")
    parser.add_argument("-k", "--top_k", type=int, default=3, help="Number of results to retrieve.")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL, help=f"OpenAI embedding model to use (default: {DEFAULT_MODEL})")
    args = parser.parse_args()

    print(f"❓ Query: {args.query}")
    print(f"   Using embedding model: {args.model}")
    
    # 1. Embed the query
    print("   Embedding query...")
    embedding_response = client.embeddings.create(
        model=args.model,
        input=[args.query]
    )
    # Handle different OpenAI library versions
    if hasattr(embedding_response, "data"):
        query_embedding = embedding_response.data[0].embedding
    results = collection.query(
        query_embeddings=[list(query_embedding)],
        n_results=args.top_k
    )
    
    # 2. Query ChromaDB
    print("   Searching database...")
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=args.top_k
    )
    
    # 3. Display results
    print("\n✅ Top Results:\n" + "="*20)
    if results.get('documents') and len(results['documents']) > 0 and len(results['documents'][0]) > 0:
        distances = results.get('distances', [[]])
        for i, doc in enumerate(results['documents'][0]):
            source = results['metadatas'][0][i].get('source', 'N/A')
            page = results['metadatas'][0][i].get('page', 'N/A')
            print(f"Source: {source}")
            print(f"Page: {page}")
            if len(distances) > 0 and len(distances[0]) > i:
                print(f"Distance: {distances[0][i]:.4f}")
            else:
                print("Distance: N/A")
            print("Text:")
            print(doc)
            print("\n")
    else:
        print("No results found.")

if __name__ == "__main__":
    main()