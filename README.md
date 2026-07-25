# Enterprise RAG Assistant

An Enterprise Retrieval-Augmented Generation (RAG) chatbot developed for **Business Gateways International (BGI)**. The assistant answers user queries by retrieving relevant information from enterprise documents and generating context-aware responses using Google's Gemini model.

---

## Features

- 📄 Supports multiple enterprise documents
- 🔍 Semantic search using Sentence Transformers
- 🧠 Retrieval-Augmented Generation (RAG)
- ⚡ FAISS vector database for fast retrieval
- 🤖 Google Gemini API for answer generation
- ✂️ Intelligent text chunking (LangChain's `RecursiveCharacterTextSplitter`)
- 📑 Source-aware responses
- 🧹 Automated document preprocessing

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python |
| LLM | Google Gemini API (`google-genai`) |
| Embedding Model | Sentence Transformers (all-MiniLM-L6-v2) |
| Vector Database | FAISS |
| Text Splitting | LangChain (`langchain_text_splitters`) |
| Document Processing | pdfplumber, JSON |
| UI | Streamlit |
| Environment | Python Virtual Environment |

---

## Project Structure

```
enterprise-rag-assistant/
│
├── data/
│   ├── raw/
│   │   └── bgi documents/          # source PDFs
│   ├── processed/
│   │   ├── extracted_text.json
│   │   ├── cleaned_text.json
│   │   └── chunks.json
│   └── vector_store/
│       ├── faiss_index.bin
│       └── metadata.pkl
│
├── src/
│   ├── app.py                # Streamlit UI
│   ├── pdf_extractor.py      # PDF -> extracted_text.json
│   ├── preprocessing.py      # cleans extracted text -> cleaned_text.json
│   ├── chunking.py           # splits text into chunks -> chunks.json
│   ├── embeddings.py         # builds FAISS index from chunks
│   ├── vector_store.py       # loads index, retrieves top-k chunks
│   ├── rag_pipeline.py       # orchestrates retrieval + generation
│   ├── gemini_client.py      # Gemini API client
│   ├── prompt_template.py    # builds grounded prompt from retrieved chunks
│   └── test_pipeline.py      # CLI script to test retrieval + generation
│
├── .env                       # API keys
├── .gitignore
├── LICENSE
└── README.md
```

---

## RAG Pipeline

```
Enterprise Documents (PDF)
        │
        ▼
pdf_extractor.py  ──▶  extracted_text.json
        │
        ▼
preprocessing.py  ──▶  cleaned_text.json
        │
        ▼
chunking.py  ──▶  chunks.json
        │
        ▼
embeddings.py  ──▶  FAISS index + metadata
        │
        ▼
User Query
        │
        ▼
vector_store.py (similarity search)
        │
        ▼
prompt_template.py (build grounded prompt)
        │
        ▼
gemini_client.py (Google Gemini)
        │
        ▼
Generated Response
```

`rag_pipeline.py` ties retrieval (`vector_store.py`) and generation (`gemini_client.py`) together into a single `ask_question()` function.

---

## Installation

### Clone the repository

```bash
git clone https://github.com/shalinir75/enterprise-rag-assistant.git
cd enterprise-rag-assistant
```

### Create a virtual environment

Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux

```bash
python -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```bash
pip install streamlit google-genai python-dotenv pdfplumber faiss-cpu sentence-transformers langchain-text-splitters
```

> No `requirements.txt` exists in the repo yet. Once your environment is set up, run `pip freeze > requirements.txt` to generate one — future setup can then use `pip install -r requirements.txt`.

---

## Environment Variables

The project reads its Gemini API key from a `.env` file in the project root:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

## Running the Pipeline

Run these once, in order, to build the knowledge base from the PDFs in `data/raw/bgi documents/`:

```bash
python src/pdf_extractor.py     # extract text from PDFs
python src/preprocessing.py     # clean extracted text
python src/chunking.py          # split into chunks
python src/embeddings.py        # embed chunks + build FAISS index
```

Then query from the command line:

```bash
python src/test_pipeline.py     # or: python src/rag_pipeline.py
```

Or launch the web UI:

```bash
streamlit run src/app.py
```

> **Note:** `app.py` currently uses hardcoded placeholder responses and is not yet wired to `rag_pipeline.py` (marked `# TODO` in the code). For real answers today, use `test_pipeline.py` or `rag_pipeline.py` directly; connecting the Streamlit UI to the pipeline is the next step.

---

## Workflow

1. Load enterprise documents (PDFs).
2. Extract text (and tables) from PDFs.
3. Clean and preprocess extracted text.
4. Split documents into semantic chunks.
5. Generate embeddings using Sentence Transformers.
6. Store embeddings in a FAISS index.
7. Accept a user query.
8. Retrieve the most relevant chunks via similarity search.
9. Build a grounded prompt from the retrieved context.
10. Generate a context-aware response using Gemini.

---

## Sample Use Cases

- HR Policy Questions
- Product Information
- Certification Guidance
- Employee Documentation
- Internal Knowledge Retrieval

---

## Project Status

🚧 Active development.

- ✅ PDF extraction, preprocessing, chunking, embeddings, FAISS retrieval, prompt building, and Gemini generation are implemented and working end-to-end via CLI (`rag_pipeline.py` / `test_pipeline.py`).
- 🔧 Streamlit UI (`app.py`) exists but still uses placeholder/mock responses — connecting it to `rag_pipeline.py` is the next step.

---

## Future Enhancements

- Wire up the Streamlit UI to the real RAG pipeline
- Support for DOCX, PPTX, and HTML documents
- Conversation history
- Multi-user authentication
- Hybrid keyword + semantic search
- Source citation highlighting

---

## License

This project is licensed under the MIT License.

---

## Team

Developed as part of the **Business Gateways International (BGI)** internship project.
