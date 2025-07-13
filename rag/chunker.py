import os
import fitz  # PyMuPDF
import json
from typing import List
from pathlib import Path

# Configuration
SOURCE_PATH = Path("knowledgebase/sources/Wyckoff_Stock_Analysis.pdf")
OUTPUT_PATH = Path("knowledgebase/chunked/Wyckoff_Stock_Analysis.json")
CHUNK_SIZE = 500  # words
OVERLAP = 100  # words


def extract_text_from_pdf(pdf_path: Path) -> str:
    doc = fitz.open(str(pdf_path))
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def chunk_text(text: str, chunk_size: int, overlap: int, source_name: str) -> List[dict]:
    words = text.split()
    chunks = []
    start = 0
    chunk_id = 0
    total_words = len(words)

    while start < total_words:
        end = min(start + chunk_size, total_words)
        chunk_words = words[start:end]
        chunk_text = " ".join(chunk_words)

        # Simulated page and section number
        estimated_page = (start // 400) + 1  # Roughly 400 words per page
        section_number = (start // 3000) + 1  # Roughly one section per ~6 pages

        chunks.append({
            "chunk_id": f"{source_name}_{chunk_id}",
            "source": source_name,
            "text": chunk_text,
            "metadata": {
                "page": estimated_page,
                "section": f"Section {section_number}"
            }
        })

        start += chunk_size - overlap
        chunk_id += 1

    return chunks

def save_chunks_to_json(chunks: List[dict], output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)


def main():
    print("🔍 Extracting text from PDF...")
    raw_text = extract_text_from_pdf(SOURCE_PATH)
    print(f"✅ Extracted {len(raw_text.split())} words")

    # Extract the source name from the file name
    source_name = SOURCE_PATH.stem

    print("✂️ Chunking text with overlap...")
    chunks = chunk_text(raw_text, CHUNK_SIZE, OVERLAP, source_name)
    print(f"✅ Created {len(chunks)} chunks")

    print(f"💾 Saving to {OUTPUT_PATH}")
    save_chunks_to_json(chunks, OUTPUT_PATH)
    print("✅ Done.")

if __name__ == "__main__":
    main()
