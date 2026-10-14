# pip install openai gradio python-dotenv
import os
import gradio as gr
from fastapi import FastAPI
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

openrouter_client = OpenAI(api_key=os.getenv("OPEN_ROUTER_API_KEY"),
                            base_url="https://openrouter.ai/api/v1")
gemini_client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta",
)

def ask(client, model, prompt):
    r = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": prompt}])
    return r.choices[0].message.content

def battle(prompt):
    a = ask(openrouter_client, "nvidia/nemotron-3.5-lightning:free", prompt)
    b = ask(gemini_client, "gemini-3.5-flash-lite", prompt)
    return a, b

def vote(label):
    return f"🗳️ Thanks! You voted: **{label}**"   # in real apps, save this to a file/DB

with gr.Blocks(title="LLM Arena") as demo:
    gr.Markdown("# 🥊 LLM Arena — one prompt, two models")
    prompt = gr.Textbox(label="Ask both models the same thing")
    go = gr.Button("⚔️ Battle!", variant="primary")

    with gr.Row():
        with gr.Column():
            gr.Markdown("### 🤖 Model A")
            out_a = gr.Markdown()
            with gr.Row():
                up_a   = gr.Button("👍");  down_a = gr.Button("👎")
        with gr.Column():
            gr.Markdown("### 🤖 Model B")
            out_b = gr.Markdown()
            with gr.Row():
                up_b   = gr.Button("👍");  down_b = gr.Button("👎")

    verdict = gr.Markdown()

    go.click(battle, inputs=prompt, outputs=[out_a, out_b])
    up_a.click(lambda: vote("👍 Model A"), outputs=verdict)
    down_a.click(lambda: vote("👎 Model A"), outputs=verdict)
    up_b.click(lambda: vote("👍 Model B"), outputs=verdict)
    down_b.click(lambda: vote("👎 Model B"), outputs=verdict)

app = gr.mount_gradio_app(FastAPI(), demo, path="/")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    demo.launch(
        server_name="0.0.0.0",
        server_port=port,
        prevent_thread_lock=False,
    )