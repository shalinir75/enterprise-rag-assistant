import json
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ==========================
# File Paths
# ==========================

input_file = Path("data/processed/cleaned_text.json")
output_file = Path("data/processed/chunks.json")

# ==========================
# Load Cleaned JSON  .\.venv\Scripts\python.exe src\chunking.py
# ==========================

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# ==========================
# Text Splitter
# ==========================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ".", " ", ""]
)

# ==========================
# Create Chunks
# ==========================

chunks = []

for pdf_name, pdf_data in data.items():

    full_text = pdf_data.get("full_text", "")

    if not full_text:
        continue

    split_chunks = text_splitter.split_text(full_text)

    for i, chunk in enumerate(split_chunks):

        chunks.append({
            "source": pdf_name,
            "chunk_id": i + 1,
            "text": chunk
        })

# ==========================
# Create Output Folder
# ==========================

output_file.parent.mkdir(parents=True, exist_ok=True)

# ==========================
# Save Chunks
# ==========================

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=4, ensure_ascii=False)

print(f"✅ Created {len(chunks)} chunks.")
print(f"✅ Saved to {output_file}")
