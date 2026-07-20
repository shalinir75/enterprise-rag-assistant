"""
pdf_extractor.py
Reads PDFs, validates them, skips duplicates, extracts text + metadata,
and saves everything to extracted_text.json.
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from pypdf import PdfReader
from pypdf.errors import PdfReadError

RAW_DATA_DIR = Path("data/raw/bgi documents")
OUTPUT_FILE = Path("data/processed/extracted_text.json")

def compute_file_hash(pdf_path: Path) -> str:
    # Used to catch duplicate files by content, not just filename
    hasher = hashlib.sha256()
    with open(pdf_path, "rb") as f:
        hasher.update(f.read())
    return hasher.hexdigest()


def validate_pdf(pdf_path: Path) -> str | None:
    # Returns an error message, or None if the file is fine
    if pdf_path.stat().st_size == 0:
        return "File is empty"
    try:
        reader = PdfReader(str(pdf_path))
        if len(reader.pages) == 0:
            return "PDF has no pages"
        if reader.is_encrypted:
            return "PDF is password-protected"
    except PdfReadError:
        return "Not a valid PDF"
    except Exception as e:
        return f"Error reading file: {e}"
    return None


def extract_pages(pdf_path: Path) -> tuple[list[dict], dict]:
    # Extracts text per page (for citations) + basic PDF metadata
    reader = PdfReader(str(pdf_path))
    pages = [
        {"page_number": i, "text": (p.extract_text() or "").strip()}
        for i, p in enumerate(reader.pages, start=1)
    ]
    meta = reader.metadata or {}
    metadata = {
        "title": meta.get("/Title", "") or "",
        "author": meta.get("/Author", "") or "",
        "creation_date": meta.get("/CreationDate", "") or "",
    }
    return pages, metadata


def extract_all_pdfs(folder: Path) -> dict:
    results = {}
    seen_hashes = {}

    for pdf_file in folder.glob("*.pdf"):
        error = validate_pdf(pdf_file)
        if error:
            print(f"Skipped {pdf_file.name}: {error}")
            continue

        file_hash = compute_file_hash(pdf_file)
        if file_hash in seen_hashes:
            print(f"Skipped {pdf_file.name}: duplicate of {seen_hashes[file_hash]}")
            continue
        seen_hashes[file_hash] = pdf_file.name

        try:
            pages, metadata = extract_pages(pdf_file)
            full_text = "\n".join(p["text"] for p in pages)
            results[pdf_file.name] = {
                "source_file": pdf_file.name,
                "file_hash": file_hash,
                "num_pages": len(pages),
                "extracted_at": datetime.now(timezone.utc).isoformat(),
                "pdf_metadata": metadata,
                "pages": pages,
                "full_text": full_text,
            }
            print(f"Extracted: {pdf_file.name} ({len(pages)} pages)")
        except Exception as e:
            print(f"Failed to extract {pdf_file.name}: {e}")

    return results


if __name__ == "__main__":
    extracted = extract_all_pdfs(RAW_DATA_DIR)
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(extracted, f, indent=2, ensure_ascii=False)
    print(f"\nDone. {len(extracted)} documents extracted -> {OUTPUT_FILE}")