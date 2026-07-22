import pickle
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# ==============================
# File Paths
# ==============================

index_file = Path("data/vector_store/faiss_index.bin")
metadata_file = Path("data/vector_store/metadata.pkl")

chunks_file = Path("data/processed/chunks.json")

# ==============================
# Load Embedding Model
# ==============================

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Model loaded.")

# ==============================
# Load FAISS Index
# ==============================

index = faiss.read_index(str(index_file))

# ==============================
# Load Metadata
# ==============================

with open(metadata_file, "rb") as f:
    metadata = pickle.load(f)

# ==============================
# Load Chunks
# ==============================

import json

with open(chunks_file, "r", encoding="utf-8") as f:
    chunks = json.load(f)

# ==============================
# User Query
# ==============================

query = input("Ask a question: ")

# ==============================
# Generate Query Embedding
# ==============================

query_embedding = model.encode(
    [query],
    convert_to_numpy=True
)

# ==============================
# Top-K Search
# ==============================

k = 3

distances, indices = index.search(
    query_embedding.astype("float32"),
    k
)

# ==============================
# Display Results
# ==============================

print("\nMost Relevant Chunks:\n")

for rank, idx in enumerate(indices[0], start=1):

    info = metadata[idx]

    chunk = chunks[idx]

    print("=" * 50)
    print(f"Rank : {rank}")
    print(f"Document : {info['document']}")
    print(f"Chunk ID : {info['chunk_id']}")
    print()
    print(chunk["text"])
    print("=" * 50)
