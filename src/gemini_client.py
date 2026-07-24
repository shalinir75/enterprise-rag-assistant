import os
import time
from dotenv import load_dotenv
from google import genai

# ==========================================
# Load API Key
# ==========================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file.")

print("API Key Loaded Successfully.")

# ==========================================
# Create Gemini Client
# ==========================================

client = genai.Client(api_key=api_key)

# ==========================================
# Generate Response Function
# ==========================================

def generate_response(question, context):
    """
    Generates an answer using Gemini based only on the retrieved context.
    """

    prompt = f"""
You are an AI assistant for Business Gateways International (BGI).

Answer ONLY using the information provided in the context below.Provide concise
and accurate answers.

If the answer is not available in the context, reply:

"I couldn't find the requested information in the available documents."

Context:
{context}

Question:
{question}

Answer:
"""

    # Retry up to 3 times if the service is temporarily unavailable
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="models/gemini-2.5-flash",
                contents=prompt
            )

            return response.text

        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")

            if attempt == 2:
                return f"Error: {e}"

            time.sleep(5)

# ==========================================
# Test
# ==========================================

if __name__ == "__main__":

    context = """
Business Gateways International provides JSRS certification services.

Applications for JSRS certification are submitted through the Support Portal.

Users must create an account before submitting their application.
"""

    question = "How do I apply for JSRS certification?"

    print("\n==============================")
    print("Generated Response")
    print("==============================\n")

    answer = generate_response(question, context)

    print(answer)
