import os
import gradio as gr
from fastapi import FastAPI
from summarizer import summarize

demo = gr.Interface(
    fn=summarize,                                  # your function
    inputs=gr.Textbox(label="Website URL"),
    outputs=gr.Markdown(label="Summary"),
    title="🔎 AI Website Summarizer",
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    demo.launch(
        server_name="0.0.0.0",   # Required: Binds to all network interfaces
        server_port=port,        # Required: Uses the port assigned dynamically by Render
        prevent_thread_lock=False # Ensures the main thread stays alive
    )

app = gr.mount_gradio_app(FastAPI(), demo, path="/")