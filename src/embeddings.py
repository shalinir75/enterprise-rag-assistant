import json
import pickle
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# ==============================
# File Paths
# ==============================

input_file = Path("data/processed/chunks.json")

index_file = Path("data/vector_store/faiss_index.bin")
metadata_file = Path("data/vector_store/metadata.pkl")

index_file.parent.mkdir(parents=True, exist_ok=True)

# ==============================
# Load Embedding Model
# ==============================

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Model loaded successfully.")

# ==============================
# Load Chunks
# ==============================

with open(input_file, "r", encoding="utf-8") as f:
    chunks = json.load(f)

texts = []
metadata = []

# ==============================
# Collect Chunk Text
# ==============================

for chunk in chunks:

    text = chunk.get("text", "").strip()

    if not text:
        continue

    texts.append(text)

    metadata.append({
        "document": chunk["source"],
        "chunk_id": chunk["chunk_id"]
    })

print(f"Collected {len(texts)} chunks.")

# ==============================
# Generate Embeddings
# ==============================

print("Generating embeddings...")

embeddings = model.encode(
    texts,
    convert_to_numpy=True,
    show_progress_bar=True
)

print("Embeddings generated.")

# ==============================
# Create FAISS Index
# ==============================

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings.astype("float32"))

print(f"Indexed {index.ntotal} vectors.")

# ==============================
# Save FAISS Index
# ==============================

faiss.write_index(index, str(index_file))

# Save metadata

with open(metadata_file, "wb") as f:
    pickle.dump(metadata, f)

print("=" * 50)
print("✅ Embeddings created successfully!")
print(f"📂 FAISS Index : {index_file}")
print(f"📂 Metadata    : {metadata_file}")
print(f"📄 Total Chunks: {len(texts)}")
print("=" * 50)
