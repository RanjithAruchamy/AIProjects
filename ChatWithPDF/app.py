from pdf_chat import ask
from pdf_loader import build_index
import gradio as gr
from fastapi import FastAPI

state = {"db": None}

def upload(pdf):
    state["db"] = build_index(pdf.name)
    return "✅ PDF indexed! Ask me anything about it."

def chat(message, history):
    if state["db"] is None:
        return "Please upload a PDF first 📄"
    return ask(state["db"], message)

with gr.Blocks(title="📄 Chat with your PDF") as demo:
    gr.Markdown("## 📄 Chat with your PDF (powered by RAG)")
    pdf    = gr.File(label="Upload a PDF", file_types=[".pdf"])
    status = gr.Markdown()
    pdf.upload(upload, inputs=pdf, outputs=status)
    gr.ChatInterface(fn=chat)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    demo.launch(
        server_name="0.0.0.0",   # Required: Binds to all network interfaces
        server_port=port,        # Required: Uses the port assigned dynamically by Render
        prevent_thread_lock=False # Ensures the main thread stays alive
    )

app = gr.mount_gradio_app(FastAPI(), demo, path="/")