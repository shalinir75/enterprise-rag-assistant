import json
from pathlib import Path
import pdfplumber

# ==========================
# File Paths
# ==========================
input_folder = Path("data/raw/bgi documents")
output_file = Path("data/processed/extracted_text.json")


# ==========================
# Table Formatting
# ==========================
def format_table(table):
    """Converts a table into readable 'Header: Value' lines."""
    if not table or len(table) < 2:
        return ""
    headers = [(h or "").strip() for h in table[0]]
    lines = []
    for row in table[1:]:
        parts = []
        for i, cell in enumerate(row):
            val = (cell or "").strip()
            if val:
                header = headers[i] if i < len(headers) and headers[i] else f"Col {i+1}"
                parts.append(f"{header}: {val}")
        if parts:
            lines.append(", ".join(parts))
    return "\n".join(lines)


# ==========================
# Extract Text from PDFs
# ==========================
data = {}

for pdf_file in sorted(input_folder.glob("*.pdf")):
    try:
        page_texts = []
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                text = (page.extract_text() or "").strip()

                # Add table content (if any) as readable "Header: Value" lines
                tables = page.extract_tables()
                table_text = "\n".join(format_table(t) for t in tables if t)
                if table_text:
                    text = f"{text}\n{table_text}".strip()

                page_texts.append(text)

        data[pdf_file.name] = {
            "full_text": "\n\n".join(page_texts)
        }
        print(f"✅ Extracted: {pdf_file.name}")
    except Exception as e:
        # One bad PDF shouldn't stop the rest of the batch
        print(f"❌ Failed to extract {pdf_file.name}: {e}")


# ==========================
# Create Output Folder
# ==========================
output_file.parent.mkdir(parents=True, exist_ok=True)


# ==========================
# Save Extracted JSON
# ==========================
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\n✅ Done. {len(data)} documents extracted -> {output_file}")