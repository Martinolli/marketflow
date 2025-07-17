"""
This script extracts text from a PDF file, chunks it into smaller pieces while preserving page numbers, and saves the result as a JSON file.
How to use:
1. Ensure you have the required libraries installed: `pip install pymupdf langchain-text-splitters`.
2. Run the script with the command:
```bash
   python rag\chunker.py "knowledgebase/sources/Wyckoff_Stock_Analysis.pdf" "knowledgebase/chunked/Wyckoff_Stock_Analysis.json"
```
"""

import fitz  # PyMuPDF
import json
import argparse
from typing import List, Dict, Tuple
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Local imports
from marketflow.marketflow_logger import get_logger
from marketflow.marketflow_config_manager import create_app_config

# Default Configuration
DEFAULT_CHUNK_SIZE = 1000  # Characters, not words. Langchain splitters use characters.
DEFAULT_CHUNK_OVERLAP = 150 # Characters

# Initialize logger and config
logger = get_logger(module_name="ChunkerData")
config = create_app_config(logger=logger)

def extract_pages_from_pdf(pdf_path: Path) -> List[Tuple[int, str]]:
    """Extracts text from each page of a PDF and returns a list of (page_number, text)."""
    logger.info(f"Opening PDF file: {pdf_path}")
    doc = fitz.open(str(pdf_path))
    pages = []
    logger.info(f"Extracting text from {len(doc)} pages in '{pdf_path.name}'...")
    for i, page in enumerate(doc):
        text = page.get_text()
        if text.strip():  # Only add pages with actual text content
            logger.debug(f"Page {i + 1}: extracted {len(text)} characters.")
            pages.append((i + 1, text))
        else:
            logger.debug(f"Page {i + 1}: no text found, skipping.")
    logger.info(f"Extracted text from {len(pages)} pages with content.")
    print(f"📄 Extracted text from {len(pages)} pages.")
    return pages

def chunk_document(pages: List[Tuple[int, str]], source_name: str, chunk_size: int, chunk_overlap: int) -> List[Dict]:
    """
    Chunks text using a semantic splitter and preserves page number metadata.
    """
    # This splitter tries to keep paragraphs/sentences together, which is better for semantics.
    logger.info(f"Chunking text with chunk size {chunk_size} and overlap {chunk_overlap}...")
    print(f"✂️ Chunking text with chunk size {chunk_size} and overlap {chunk_overlap}...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        add_start_index=True, # This helps in ordering if needed
    )

    all_chunks = []
    chunk_id_counter = 0

    for page_number, page_text in pages:
        # Split the text of a single page
        page_chunks = text_splitter.split_text(page_text)

        for chunk_text in page_chunks:
            chunk_id = f"{source_name}_{chunk_id_counter}"
            all_chunks.append({
                "chunk_id": chunk_id,
                "source": source_name,
                "text": chunk_text,
                "metadata": {
                    "page": page_number,
                    # You can add more metadata here if you can extract it
                    # "section": "..."
                }
            })
            chunk_id_counter += 1
            logger.debug(f"Created chunk {chunk_id} from page {page_number} with {len(chunk_text)} characters.")

    logger.info(f"Created {len(all_chunks)} chunks from the document.")
    print(f"✅ Created {len(all_chunks)} chunks from the document.")
            
    return all_chunks

def save_chunks_to_json(chunks: List[Dict], output_path: Path):
    """Saves a list of chunks to a JSON file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    logger.info(f"Saving {len(chunks)} chunks to {output_path}")
    print(f"💾 Saving {len(chunks)} chunks to {output_path}")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)
    print(f"💾 Saved {len(chunks)} chunks to {output_path}")

def main():
    logger.info("Starting the chunking process...")
    print("🔍 Starting the chunking process...")
    parser = argparse.ArgumentParser(description="Extract text from a PDF, chunk it, and save to JSON.")
    parser.add_argument("source_path", type=Path, help="Path to the source PDF file.")
    parser.add_argument("output_path", type=Path, help="Path to the output JSON file.")
    parser.add_argument("--chunk_size", type=int, default=DEFAULT_CHUNK_SIZE, help="The target size for each chunk in characters.")
    parser.add_argument("--overlap", type=int, default=DEFAULT_CHUNK_OVERLAP, help="The overlap between consecutive chunks in characters.")
    args = parser.parse_args()

    print("🔍 Starting chunking process...")
    logger.info(f"Chunking PDF: {args.source_path} with chunk size {args.chunk_size} and overlap {args.overlap}")
    
    # 1. Extract text page by page with real page numbers
    pages = extract_pages_from_pdf(args.source_path)
    if not pages:
        print("❌ No text could be extracted from the PDF. Exiting.")
        return

    # 2. Get the source name from the file
    source_name = args.source_path.stem

    # 3. Perform semantic chunking
    print(f"✂️ Chunking text with chunk size {args.chunk_size} and overlap {args.overlap}...")
    chunks = chunk_document(pages, source_name, args.chunk_size, args.overlap)
    logger.info(f"Chunking complete. Created {len(chunks)} chunks.")
    
    # 4. Save the result
    save_chunks_to_json(chunks, args.output_path)
    logger.info(f"Chunking process completed successfully. Output saved to {args.output_path}")
    print("✅ Done.")

if __name__ == "__main__":
    main()