import pickle
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import json

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

with open(chunks_file, "r", encoding="utf-8") as f:
    chunks = json.load(f)

# ==============================
# Retrieval Function
# ==============================

def retrieve_chunks(query, k=3):

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

    distances, indices = index.search(
        query_embedding.astype("float32"),
        k
    )

    # ==============================
    # Build Results List
    # ==============================

    results = []

    for idx in indices[0]:

        if idx == -1:
            continue

        info = metadata[idx]
        chunk = chunks[idx]

        results.append({
            "source": info["document"],     # <-- renamed from "document" to "source"
            "chunk_id": info["chunk_id"],
            "text": chunk["text"]
        })

    return results


# ==============================
# Standalone Test
# ==============================

if __name__ == "__main__":

    query = input("Ask a question: ")

    results = retrieve_chunks(query)

    print("\nMost Relevant Chunks:\n")

    for rank, r in enumerate(results, start=1):

        print("=" * 50)
        print(f"Rank : {rank}")
        print(f"Source : {r['source']}")
        print(f"Chunk ID : {r['chunk_id']}")
        print()
        print(r["text"])
        print("=" * 50)
