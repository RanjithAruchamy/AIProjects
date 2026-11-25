# 📂 MultiFormatChat

A **RAG (Retrieval-Augmented Generation)** web app that lets you upload multiple documents and chat with their contents. Built with Google Gemini, LangChain, ChromaDB, and Gradio.

## Supported Formats

| Format | Extension | Notes |
|--------|-----------|-------|
| PDF | `.pdf` | Page-aware; max 50 pages per file |
| Word | `.docx` | Full document text |
| Excel | `.xlsx`, `.xls` | Each sheet indexed separately |
| Markdown | `.md` | Full text |
| Plain Text | `.txt` | Full text |

## Limits

- **Max 5 files** per session
- **Max 10 MB** per file
- **Max 50 pages** for PDFs
- **Max 1,500 total chunks** across all files

## Project Structure

```
MultiFormatChat/
├── app.py            # Gradio UI + FastAPI mount
├── doc_loader.py     # File loading, chunking & Chroma indexing
├── doc_chat.py       # RAG Q&A chain (Gemini LLM)
├── requirements.txt  # Dependencies
└── README.md
```

## Setup

### 1. Create & activate a virtual environment
```bash
cd MultiFormatChat
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API key
Ensure your `.env` file at the repo root contains:
```
GOOGLE_API_KEY=your_google_api_key_here
```

### 4. Run the app
```bash
python app.py
```
Then open **http://localhost:7860** in your browser.

## How It Works

```
Upload Files
    │
    ▼
doc_loader.py ──► PyPDFLoader / Docx2txtLoader / pandas / plain-text
    │
    ▼
RecursiveCharacterTextSplitter  (800 chars, 100 overlap)
    │
    ▼
GoogleGenerativeAIEmbeddings  (gemini-embedding-001)
    │
    ▼
ChromaDB  (in-memory vector store)
    │
    ▼  (on each question)
Similarity Search  (top 5 chunks)
    │
    ▼
Gemini LLM  (gemini-3.5-flash-lite)  +  strict context prompt
    │
    ▼
Answer  +  Source citations (filename + page/sheet)
```

## Deployment (Render)

The `app` variable in `app.py` is a FastAPI + Gradio mount, ready for Render.
Set the `PORT` environment variable and point Render to `uvicorn app:app`.
