"""
pdf_extractor.py
Member 1's task: unzip documents, read all PDFs with PyPDF, extract
text, and save it as JSON for Member 2 to clean.
"""

import json
from pathlib import Path
from pypdf import PdfReader

# Folder where your PDFs live
RAW_DATA_DIR = Path("data/raw/bgi documents")
OUTPUT_FILE = Path("data/processed/extracted_text.json")


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extract all text from a single PDF file."""
    reader = PdfReader(str(pdf_path))
    text = ""
    for page in reader.pages:
        text += (page.extract_text() or "") + "\n"
    return text.strip()


def extract_all_pdfs(folder: Path) -> dict:
    """
    Extract text from every PDF in the folder.
    Returns {filename: extracted_text}
    """
    results = {}
    pdf_files = list(folder.glob("*.pdf"))

    if not pdf_files:
        print(f"No PDFs found in {folder}")
        return results

    for pdf_file in pdf_files:
        try:
            text = extract_text_from_pdf(pdf_file)
            results[pdf_file.name] = text
            print(f"Extracted: {pdf_file.name} ({len(text)} characters)")
        except Exception as e:
            print(f"Failed to extract {pdf_file.name}: {e}")

    return results


def save_as_json(data: dict, output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\nSaved extracted text to {output_path}")


if __name__ == "__main__":
    extracted = extract_all_pdfs(RAW_DATA_DIR)
    save_as_json(extracted, OUTPUT_FILE)
    print(f"\nDone. {len(extracted)} documents extracted.")