"""
rag_pipeline.py

Central backend orchestrator for the Enterprise RAG Assistant.

The UI should ONLY interact with this file.
"""

from vector_store import retrieve_chunks
from gemini_client import generate_response


def ask_question(question, k=3):
    """
    Complete RAG pipeline.

    Returns:
        {
            "answer": "...",
            "chunks": [...],
            "sources": [...]
        }
    """

    # Validate input
    if not question.strip():
        return {
            "answer": "Please enter a question.",
            "chunks": [],
            "sources": []
        }

    # Retrieve chunks
    try:
        chunks = retrieve_chunks(question, k)

    except Exception as e:
        return {
            "answer": f"Retrieval Error: {str(e)}",
            "chunks": [],
            "sources": []
        }

    # No chunks found
    if not chunks:
        return {
            "answer": "I couldn't find relevant information in the knowledge base.",
            "chunks": [],
            "sources": []
        }

    # Extract unique sources
    sources = []

    for chunk in chunks:
        if chunk["source"] not in sources:
            sources.append(chunk["source"])

    # Build context
    context = ""

    for chunk in chunks:
        context += (
            f"Source: {chunk['source']}\n"
            f"{chunk['text']}\n\n"
        )

    # Generate response
    try:
        answer = generate_response(question, context)

    except Exception as e:
        return {
            "answer": f"Generation Error: {str(e)}",
            "chunks": chunks,
            "sources": sources
        }

    return {
        "answer": answer,
        "chunks": chunks,
        "sources": sources
    }
# ==========================================
# Test
# ==========================================

if __name__ == "__main__":

        question = input("Ask a question: ")

        result = ask_question(question)

        print("\n" + "=" * 50)
        print("Answer:")
        print("=" * 50)
        print(result["answer"])

        print("\nSources:")
        for source in result["sources"]:
            print("-", source)
