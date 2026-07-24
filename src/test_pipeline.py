from vector_store import retrieve_chunks
from gemini_client import generate_response


def main():
    question = input("Ask a question: ")

    # Step 1: Retrieve relevant chunks
    results = retrieve_chunks(question, k=3)

    print("\n" + "=" * 50)
    print("RETRIEVED CHUNKS")
    print("=" * 50)
    for r in results:
        print(f"- {r['source']} (Chunk {r['chunk_id']})")
        print(r['text'][:150], "...\n")

    # Step 2: Build context string from retrieved chunks
    context = "\n\n".join(
        f"Source: {r['source']} (Chunk {r['chunk_id']})\n{r['text']}"
        for r in results
    )

    # Step 3: Get Gemini's answer
    answer = generate_response(question, context)

    print("=" * 50)
    print("ANSWER")
    print("=" * 50)
    print(answer)


if __name__ == "__main__":
    main()
