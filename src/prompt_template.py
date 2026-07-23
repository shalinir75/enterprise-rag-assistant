
# ==============================
# Prompt Template
# ==============================

PROMPT_TEMPLATE = """Answer the question using only the context provided below. Do not use outside knowledge.

Context:
{context}

Question: {question}

Rules:
- Base your answer strictly on the context above.
- If the context does not contain the answer, respond exactly with: "I don't have enough information to answer that."
- Keep the answer short and to the point (2-4 sentences unless more detail is explicitly asked for).
- Do not repeat the question or mention "the context" in your answer.

Answer:"""


# ==============================
# Build Prompt Function
# ==============================

def build_prompt(retrieved_chunks, question):

    context_parts = []

    for chunk in retrieved_chunks:
        context_parts.append(chunk["text"])

    context = "\n\n".join(context_parts)

    prompt = PROMPT_TEMPLATE.format(context=context, question=question)

    return prompt


# ==============================
# Quick Test
# ==============================

if __name__ == "__main__":

    sample_chunks = [
        {"text": "BGI was founded to provide business consulting services."},
        {"text": "The company is headquartered in Chennai, India."}
    ]

    sample_question = "Where is BGI headquartered?"

    final_prompt = build_prompt(sample_chunks, sample_question)

    print(final_prompt)