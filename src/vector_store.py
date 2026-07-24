import json
import pickle
from pathlib import Path

try:
    import faiss
except ImportError:
    faiss = None

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

# ==========================================================
# File Paths
# ==========================================================

index_file = Path("data/vector_store/faiss_index.bin")
metadata_file = Path("data/vector_store/metadata.pkl")
chunks_file = Path("data/processed/chunks.json")

# ==========================================================
# Global Resources (Loaded Only Once)
# ==========================================================

model = None
index = None
metadata = None
chunks = None


# ==========================================================
# Load Resources
# ==========================================================

def _load_resources():
    """
    Loads the embedding model, FAISS index,
    metadata and chunks only once.
    """

    global model, index, metadata, chunks

    # Load embedding model
    if model is None:

        if SentenceTransformer is None:
            raise ImportError(
                "sentence-transformers is not installed."
            )

        print("Loading embedding model...")

        model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        print("Embedding model loaded.")

    # Load FAISS
    if index is None:

        if faiss is None:
            raise ImportError(
                "faiss-cpu is not installed."
            )

        if not index_file.exists():
            raise FileNotFoundError(
                f"FAISS index not found:\n{index_file}"
            )

        print("Loading FAISS index...")

        index = faiss.read_index(
            str(index_file)
        )

        print("FAISS index loaded.")

    # Load metadata
    if metadata is None:

        if not metadata_file.exists():
            raise FileNotFoundError(
                f"Metadata file not found:\n{metadata_file}"
            )

        with open(
            metadata_file,
            "rb"
        ) as f:

            metadata = pickle.load(f)

    # Load chunks
    if chunks is None:

        if not chunks_file.exists():
            raise FileNotFoundError(
                f"Chunks file not found:\n{chunks_file}"
            )

        with open(
            chunks_file,
            "r",
            encoding="utf-8"
        ) as f:

            chunks = json.load(f)


# ==========================================================
# Retrieval Function
# ==========================================================

def retrieve_chunks(query, k=3):
    """
    Retrieves the top-k most relevant chunks.
    """

    _load_resources()

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    )

    distances, indices = index.search(
        query_embedding.astype("float32"),
        k
    )

    results = []

    for position, idx in enumerate(indices[0]):

        if idx == -1:
            continue

        results.append(
            {
                "source": metadata[idx]["document"],
                "chunk_id": metadata[idx]["chunk_id"],
                "text": chunks[idx]["text"],
                "score": float(distances[0][position])
            }
        )

    return results


# ==========================================================
# Standalone Testing
# ==========================================================

if __name__ == "__main__":

    while True:

        question = input("\nAsk a question (or type exit): ")

        if question.lower() == "exit":
            break

        try:

            results = retrieve_chunks(question)

            print("\nRetrieved Chunks:\n")

            for i, chunk in enumerate(results, start=1):

                print("=" * 60)
                print(f"Rank      : {i}")
                print(f"Source    : {chunk['source']}")
                print(f"Chunk ID  : {chunk['chunk_id']}")
                print(f"Score     : {chunk['score']:.4f}")
                print()
                print(chunk["text"])
                print("=" * 60)

        except Exception as e:

            print(f"\nError: {e}")
