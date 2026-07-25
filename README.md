# Enterprise RAG Assistant

An Enterprise Retrieval-Augmented Generation (RAG) chatbot developed for **Business Gateways International (BGI)**. The assistant answers user queries by retrieving relevant information from enterprise documents and generating context-aware responses using Google's Gemini model.

---

## Features

- 📄 Supports multiple enterprise documents
- 🔍 Semantic search using Sentence Transformers
- 🧠 Retrieval-Augmented Generation (RAG)
- ⚡ FAISS vector database for fast retrieval
- 🤖 Google Gemini API for answer generation
- ✂️ Intelligent text chunking
- 📑 Source-aware responses
- 🧹 Automated document preprocessing

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python |
| LLM | Google Gemini API |
| Embedding Model | Sentence Transformers (all-MiniLM-L6-v2) |
| Vector Database | FAISS |
| Framework | LangChain |
| Document Processing | PyPDF, JSON |
| Environment | Python Virtual Environment |

---

## Project Structure

```
enterprise-rag-assistant/
│
├── data/
│   ├── raw/
│   │   └── bgi documents/
│   ├── processed/
│   │   ├── extracted_text.json
│   │   ├── cleaned_text.json
│   │   └── chunks.json
│   └── vector_store/
│       ├── faiss_index.bin
│       └── metadata.pkl
│
├── src/
│   ├── app.py
│   ├── pdf_extractor.py
│   ├── preprocessing.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── rag_pipeline.py
│   ├── gemini_client.py
│   ├── prompt_template.py
│   └── test_pipeline.py
│
├── .env
├── .gitignore
├── LICENSE
├── README.md
└── test_env.py
```

---

## RAG Pipeline

```
Enterprise Documents
        │
        ▼
Document Extraction
        │
        ▼
Text Cleaning & Preprocessing
        │
        ▼
Text Chunking
        │
        ▼
Sentence Embeddings
        │
        ▼
FAISS Vector Store
        │
        ▼
User Query
        │
        ▼
Similarity Search
        │
        ▼
Relevant Context
        │
        ▼
Google Gemini
        │
        ▼
Generated Response
```

---

## Installation

### Clone the repository

```bash
git clone https://github.com/shalinir75/enterprise-rag-assistant.git
```

```bash
cd enterprise-rag-assistant
```

### Create a virtual environment

Windows

```bash
python -m venv .venv
```

Activate

```bash
.venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root.

```env
GOOGLE_API_KEY=YOUR_API_KEY
```

---

## Running the Pipeline

Extract documents

```bash
python src/pdf_extractor.py
```

Preprocess documents

```bash
python src/preprocessing.py
```

Chunk text

```bash
python src/chunking.py
```

Generate embeddings

```bash
python src/embeddings.py
```

Run the chatbot

```bash
python src/app.py
```

---

## Workflow

1. Load enterprise documents.
2. Extract text from PDFs.
3. Clean and preprocess extracted text.
4. Split documents into semantic chunks.
5. Generate embeddings using Sentence Transformers.
6. Store embeddings in FAISS.
7. Accept user query.
8. Retrieve the most relevant chunks.
9. Generate a context-aware response using Gemini.

---

## Sample Use Cases

- HR Policy Questions
- Product Information
- Certification Guidance
- Employee Documentation
- Internal Knowledge Retrieval

---

## Future Enhancements

- Support for DOCX, PPTX, and HTML documents
- Streamlit web interface
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
