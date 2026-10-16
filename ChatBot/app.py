# app.py
# Block 12 — the PROJECT: give your agent a chat UI with Gradio.
# Run:  python app.py     then open the local link it prints.
import gradio as gr
from agent import agent          # the function from agent.py
from fastapi import FastAPI


def chat(message, history):
    # Gradio fills in `message` (newest) and `history` (past turns) for you.
    # Homework hint: pass `history` into your agent to give it memory!
    return agent(message)


demo = gr.ChatInterface(
    fn=chat,
    title="🛍️ Smart Shop Assistant",
    description="Ask me the price of shoes, hat, bag, shorts or pants — I'll look it up.",
)
demo.launch(share=True,
            server_name="0.0.0.0",   # Required: Binds to all network interfaces
            server_port=port,        # Required: Uses the port assigned dynamically by Render
        prevent_thread_lock=False # Ensures the main thread stays alive,
        )   # share=True -> also prints a public link you can post

app = gr.mount_gradio_app(FastAPI(), demo, path="/")