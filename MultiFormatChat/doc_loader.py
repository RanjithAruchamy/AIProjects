"""
doc_loader.py
Handles loading, chunking, and indexing of multiple document types:
  PDF  (.pdf)   – PyPDFLoader (page-aware)
  Word (.docx)  – Docx2txtLoader
  Excel(.xlsx / .xls) – pandas (sheet-aware)
  Markdown/Text (.md / .txt) – plain text read
"""

import os
import pandas as pd
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

# ── Limits ──────────────────────────────────────────────────────────────────
MAX_FILES            = 5
MAX_FILE_SIZE_BYTES  = 10 * 1024 * 1024   # 10 MB per file
MAX_PDF_PAGES        = 50
MAX_CHUNKS_TOTAL     = 1500               # across all uploaded files
CHUNK_SIZE           = 800
CHUNK_OVERLAP        = 100
CHUNK_BATCH_SIZE     = 32

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".xlsx", ".xls", ".md", ".txt"}


# ── Per-format loaders ───────────────────────────────────────────────────────

def _load_pdf(path: str, filename: str) -> list[Document]:
    pages = PyPDFLoader(path).load()
    if len(pages) > MAX_PDF_PAGES:
        raise ValueError(
            f"'{filename}' has {len(pages)} pages — limit is {MAX_PDF_PAGES}."
        )
    for doc in pages:
        doc.metadata["filename"] = filename
    return pages


def _load_docx(path: str, filename: str) -> list[Document]:
    docs = Docx2txtLoader(path).load()
    for i, doc in enumerate(docs):
        doc.metadata["filename"] = filename
        doc.metadata["page"] = i          # section index
    return docs


def _load_xlsx(path: str, filename: str) -> list[Document]:
    docs = []
    xl = pd.ExcelFile(path)
    for sheet_name in xl.sheet_names:
        df = xl.parse(sheet_name)
        # Convert the sheet to a readable text table
        text = f"Sheet: {sheet_name}\n\n{df.to_string(index=False)}"
        docs.append(Document(
            page_content=text,
            metadata={"filename": filename, "page": sheet_name}
        ))
    return docs


def _load_text(path: str, filename: str) -> list[Document]:
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        content = fh.read()
    return [Document(
        page_content=content,
        metadata={"filename": filename, "page": 0}
    )]


def _load_file(path: str, filename: str) -> list[Document]:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        return _load_pdf(path, filename)
    elif ext == ".docx":
        return _load_docx(path, filename)
    elif ext in (".xlsx", ".xls"):
        return _load_xlsx(path, filename)
    elif ext in (".md", ".txt"):
        return _load_text(path, filename)
    else:
        raise ValueError(f"Unsupported file type: '{ext}'")


# ── Public API ───────────────────────────────────────────────────────────────

def build_index(file_paths: list[str]) -> tuple:
    """
    Load, chunk, embed, and index all given files into a Chroma vector store.

    Returns:
        (db, file_summaries) where file_summaries is a list of human-readable
        strings describing what was indexed per file.
    Raises:
        ValueError for any limit violation or unsupported format.
    """
    if not file_paths:
        raise ValueError("No files provided.")
    if len(file_paths) > MAX_FILES:
        raise ValueError(
            f"Too many files. Maximum {MAX_FILES} allowed, got {len(file_paths)}."
        )

    # Validate extensions upfront
    invalid = [
        os.path.basename(p)
        for p in file_paths
        if os.path.splitext(p)[1].lower() not in SUPPORTED_EXTENSIONS
    ]
    if invalid:
        raise ValueError(
            f"Unsupported file type(s): {', '.join(invalid)}. "
            f"Supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )
    embedder = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    db = Chroma(embedding_function=embedder)

    all_chunks: list[Document] = []
    file_summaries: list[str] = []

    for path in file_paths:
        filename = os.path.basename(path)

        size = os.path.getsize(path)
        if size > MAX_FILE_SIZE_BYTES:
            raise ValueError(
                f"'{filename}' is {size // (1024*1024)} MB — limit is 10 MB."
            )

        docs   = _load_file(path, filename)
        chunks = splitter.split_documents(docs)
        all_chunks.extend(chunks)
        file_summaries.append(f"✅ **{filename}** — {len(chunks)} chunks indexed")

    if not all_chunks:
        raise ValueError("No readable text found in the uploaded files.")

    if len(all_chunks) > MAX_CHUNKS_TOTAL:
        raise ValueError(
            f"Combined documents produced {len(all_chunks)} chunks, "
            f"which exceeds the {MAX_CHUNKS_TOTAL} limit. "
            "Try uploading fewer or smaller files."
        )

    # Batch-add to Chroma to stay within embedding API rate limits
    for i in range(0, len(all_chunks), CHUNK_BATCH_SIZE):
        db.add_documents(all_chunks[i : i + CHUNK_BATCH_SIZE])

    return db, file_summaries
