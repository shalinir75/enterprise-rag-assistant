import json
import pickle
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


# File Paths
<<<<<<< HEAD

input_file = Path("data/processed/cleaned_text.json")
=======
# ==============================

input_file = Path("data/processed/chunks.json")
>>>>>>> b5863c1e2aa15d47de59f7c34bef0702c99fa274

index_file = Path("data/vector_store/faiss_index.bin")
metadata_file = Path("data/vector_store/metadata.pkl")

index_file.parent.mkdir(parents=True, exist_ok=True)

# Load Embedding Model
<<<<<<< HEAD
=======
# ==============================
>>>>>>> b5863c1e2aa15d47de59f7c34bef0702c99fa274

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Model loaded successfully.")

<<<<<<< HEAD

# Load Cleaned Documents
=======
# ==============================
# Load Chunks
# ==============================
>>>>>>> b5863c1e2aa15d47de59f7c34bef0702c99fa274

with open(input_file, "r", encoding="utf-8") as f:
    chunks = json.load(f)

texts = []
metadata = []

<<<<<<< HEAD
# Extract Page Text

for pdf_name, pdf_data in documents.items():
=======
# ==============================
# Collect Chunk Text
# ==============================
>>>>>>> b5863c1e2aa15d47de59f7c34bef0702c99fa274

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


# Generate Embeddings
<<<<<<< HEAD
=======
# ==============================
>>>>>>> b5863c1e2aa15d47de59f7c34bef0702c99fa274

print("Generating embeddings...")

embeddings = model.encode(
    texts,
    convert_to_numpy=True,
    show_progress_bar=True
)

print("Embeddings generated.")


# Create FAISS Index
<<<<<<< HEAD
=======
# ==============================
>>>>>>> b5863c1e2aa15d47de59f7c34bef0702c99fa274

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings.astype("float32"))

print(f"Indexed {index.ntotal} vectors.")

<<<<<<< HEAD
# Save Index
=======
# ==============================
# Save FAISS Index
# ==============================
>>>>>>> b5863c1e2aa15d47de59f7c34bef0702c99fa274

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
