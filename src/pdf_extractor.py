"""
pdf_extractor.py
Reads PDFs and extracts text + structured tables, saving everything to
extracted_text.json.
"""
import json
from datetime import datetime, timezone
from pathlib import Path
import pdfplumber

RAW_DATA_DIR = Path("data/raw/bgi documents")
OUTPUT_FILE = Path("data/processed/extracted_text.json")


def format_table_to_text(table: list[list[str]]) -> str:
    """Converts a raw 2D grid table into structured key-value lines."""
    if not table or len(table) < 2:
        return ""

    headers = [(h or "").strip() for h in table[0]]
    formatted_rows = []

    for row in table[1:]:
        row_cells = []
        for i, cell in enumerate(row):
            val = (cell or "").strip()
            if not val:
                continue
            header_name = headers[i] if i < len(headers) and headers[i] else f"Col {i+1}"
            row_cells.append(f"{header_name}: {val}")

        if row_cells:
            formatted_rows.append(", ".join(row_cells))

    return "\n".join(formatted_rows)


def extract_page_content(page) -> str:
    """Extracts plain text and structures any tabular data on the page."""
    plain_text = (page.extract_text() or "").strip()

    try:
        tables = page.extract_tables()
    except Exception:
        tables = []

    formatted_tables = [format_table_to_text(t) for t in tables if t]
    formatted_tables = [t for t in formatted_tables if t]

    if formatted_tables:
        return f"{plain_text}\n{chr(10).join(formatted_tables)}".strip()

    return plain_text


def extract_pages(pdf_path: Path) -> tuple[list[dict], dict]:
    """Loops through PDF pages using pdfplumber for high-fidelity extraction."""
    pages = []

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            page_text = extract_page_content(page)
            pages.append({"page_number": i, "text": page_text})

    metadata = {
        "title": pdf_path.stem  # Directly uses doc name (e.g., 'jsrs_mandatory_documents')
    }

    return pages, metadata


def extract_all_pdfs(folder: Path) -> dict:
    results = {}

    if not folder.exists():
        print(f"Error: Directory '{folder}' does not exist.")
        return results

    for pdf_file in sorted(list(folder.glob("*.pdf"))):
        try:
            pages, metadata = extract_pages(pdf_file)
            full_text = "\n\n".join(p["text"] for p in pages)

            results[pdf_file.name] = {
                "source_file": pdf_file.name,
                "num_pages": len(pages),
                "extracted_at": datetime.now(timezone.utc).isoformat(),
                "pdf_metadata": metadata,
                "pages": pages,
                "full_text": full_text,
            }
            print(f"✅ Extracted: {pdf_file.name} ({len(pages)} pages)")
        except Exception as e:
            print(f"❌ Failed to extract {pdf_file.name}: {e}")

    return results


if __name__ == "__main__":
    extracted = extract_all_pdfs(RAW_DATA_DIR)
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(extracted, f, indent=2, ensure_ascii=False)

    print(f"\nDone. {len(extracted)} documents extracted -> {OUTPUT_FILE}")
    