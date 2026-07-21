import json
import pickle
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


# File Paths

input_file = Path("data/processed/cleaned_text.json")

index_file = Path("data/vector_store/faiss_index.bin")
metadata_file = Path("data/vector_store/metadata.pkl")

# Create output folder
index_file.parent.mkdir(parents=True, exist_ok=True)

# Load Embedding Model

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Model loaded successfully.")


# Load Cleaned Documents

with open(input_file, "r", encoding="utf-8") as f:
    documents = json.load(f)

texts = []
metadata = []

# Extract Page Text

for pdf_name, pdf_data in documents.items():

    pages = pdf_data.get("pages", [])

    for page in pages:

        text = page.get("text", "").strip()

        if text:

            texts.append(text)

            metadata.append({
                "document": pdf_name,
                "page": page["page_number"]
            })

print(f"Collected {len(texts)} pages.")


# Generate Embeddings

print("Generating embeddings...")

embeddings = model.encode(
    texts,
    convert_to_numpy=True,
    show_progress_bar=True
)

print("Embeddings generated.")


# Create FAISS Index

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings.astype("float32"))

print(f"Indexed {index.ntotal} vectors.")

# Save Index

faiss.write_index(index, str(index_file))

# Save metadata
with open(metadata_file, "wb") as f:
    pickle.dump(metadata, f)

print("======================================")
print("FAISS index saved.")
print(index_file)

print("Metadata saved.")
print(metadata_file)
print("======================================")