"""
doc_chat.py
RAG Q&A chain for multi-document chat.
Retrieves the top-k most relevant chunks from the vector store
and answers the user's question strictly from that context,
citing the source file name and page / sheet.
"""

import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

# ── Model ────────────────────────────────────────────────────────────────────
model = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

# ── Prompt ───────────────────────────────────────────────────────────────────
prompt = ChatPromptTemplate.from_template("""
You are a helpful document assistant. Answer the question using ONLY the context below.
If the context does not contain the answer, say "I couldn't find that in the uploaded documents."
After your answer, always list the sources you used as:
  Sources: <filename> (page X), <filename> (sheet Y), ...

Context:
{context}

Question: {question}
""")


# ── Helpers ──────────────────────────────────────────────────────────────────

def _format_source(metadata: dict) -> str:
    """Return a human-readable source label for a chunk's metadata."""
    filename = metadata.get("filename", "unknown")
    page     = metadata.get("page", "?")
    if isinstance(page, int):
        # PDF pages are 0-indexed; DOCX section index also 0-indexed
        return f"{filename} (page {page + 1})"
    else:
        # Excel sheet name (string)
        return f"{filename} (sheet: {page})"


def _build_context(chunks) -> str:
    parts = []
    for chunk in chunks:
        source = _format_source(chunk.metadata)
        parts.append(f"[{source}]\n{chunk.page_content}")
    return "\n\n---\n\n".join(parts)


# ── Public API ───────────────────────────────────────────────────────────────

def ask(db, question: str, k: int = 5) -> str:
    """
    Retrieve the most relevant chunks from *db* and answer *question*.

    Args:
        db:       Chroma vector store built by doc_loader.build_index()
        question: User's natural-language question
        k:        Number of chunks to retrieve (default 5 for multi-doc coverage)

    Returns:
        Answer string with inline source citations.
    """
    chunks  = db.similarity_search(question, k=k)
    context = _build_context(chunks)
    chain   = prompt | model
    return chain.invoke({"context": context, "question": question}).content
