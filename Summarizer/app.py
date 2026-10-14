import gradio as gr
from fastapi import FastAPI
from summarizer import summarize

demo = gr.Interface(
    fn=summarize,                                  # your function
    inputs=gr.Textbox(label="Website URL"),
    outputs=gr.Markdown(label="Summary"),
    title="🔎 AI Website Summarizer",
)

app = gr.mount_gradio_app(FastAPI(), demo, path="/")