"""
app.py
Gradio web UI for multi-format document chat.
Supports up to 5 files: PDF, DOCX, XLSX/XLS, MD, TXT.
"""

import os
import gradio as gr
from fastapi import FastAPI

from doc_loader import build_index, MAX_FILES, SUPPORTED_EXTENSIONS
from doc_chat import ask

# ── Shared mutable state (one vector store per session) ──────────────────────
state = {"db": None}

ACCEPT = [".pdf", ".docx", ".xlsx", ".xls", ".md", ".txt"]


# ── Handlers ─────────────────────────────────────────────────────────────────

def upload_files(files):
    """Index the uploaded files and update status."""
    if not files:
        return "⚠️ Please select at least one file before clicking **Index Files**."

    if len(files) > MAX_FILES:
        return (
            f"⚠️ You uploaded **{len(files)} files** but the maximum is **{MAX_FILES}**. "
            "Please remove some files and try again."
        )

    # Validate extensions
    file_paths = [f.name for f in files]
    invalid = [
        os.path.basename(p)
        for p in file_paths
        if os.path.splitext(p)[1].lower() not in SUPPORTED_EXTENSIONS
    ]
    if invalid:
        return (
            f"⚠️ Unsupported file type(s): **{', '.join(invalid)}**\n\n"
            f"Supported formats: `{', '.join(sorted(SUPPORTED_EXTENSIONS))}`"
        )

    try:
        db, summaries = build_index(file_paths)
        state["db"] = db
        summary_md = "\n".join(summaries)
        return (
            f"### ✅ Indexing complete — {len(files)} file(s) ready\n\n"
            f"{summary_md}\n\n"
            "_Ask me anything about the uploaded documents below._"
        )
    except Exception as exc:
        state["db"] = None
        return f"### ❌ Indexing failed\n\n{exc}"


def chat(message: str, history: list) -> str:
    """Answer the user's question using the indexed documents."""
    if state["db"] is None:
        return "⚠️ No documents indexed yet. Please upload and index files first."
    if not message.strip():
        return "⚠️ Please type a question."
    return ask(state["db"], message)


def reset():
    """Clear the current index so the user can start over."""
    state["db"] = None
    return None, "🗑️ Cleared. Upload new documents to start a fresh session."


# ── UI ────────────────────────────────────────────────────────────────────────

with gr.Blocks(title="📂 Multi-Format Document Chat") as demo:

    gr.Markdown(
        """
# 📂 Multi-Format Document Chat
Chat with up to **5 documents** at once — PDF, Word, Excel, Markdown, or plain text.
> Powered by **Google Gemini** + **LangChain RAG**
        """
    )

    with gr.Row():
        file_upload = gr.File(
            label=f"Upload up to {MAX_FILES} documents  (PDF · DOCX · XLSX · MD · TXT)",
            file_count="multiple",
            file_types=ACCEPT,
            scale=4,
        )

    with gr.Row():
        index_btn = gr.Button("📤 Index Files", variant="primary", scale=1)
        reset_btn = gr.Button("🗑️ Clear & Reset", variant="secondary", scale=1)

    status = gr.Markdown(
        value="_Upload files and click **Index Files** to begin._"
    )

    gr.Markdown("---")
    gr.Markdown("### 💬 Ask a question about your documents")

    gr.ChatInterface(fn=chat)

    # ── Wire events ──────────────────────────────────────────────────────────
    index_btn.click(fn=upload_files, inputs=file_upload,  outputs=status)
    reset_btn.click(fn=reset,        inputs=None,          outputs=[file_upload, status])


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    demo.launch(
        server_name="0.0.0.0",
        server_port=port,
        prevent_thread_lock=False,
    )

# FastAPI mount (for Render / cloud deployment)
app = gr.mount_gradio_app(FastAPI(), demo, path="/")
