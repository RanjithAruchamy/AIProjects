# AI Engineering · Class 2 — LangChain & Your First Agent (runnable code)

Every file here matches a code block from the Class 2 deck. They are
self-contained — run any one of them directly.

## One-time setup
```bash
# From the repository root, activate the existing project environment
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# Install Class 2 dependencies into that environment
python -m pip install -r class2/requirements.txt

# Set your key before running a script (PowerShell: $env:OPENAI_API_KEY="...")
export OPENAI_API_KEY="your_openai_api_key"
```
Get a key at https://platform.openai.com/api-keys (add a little billing credit).

In VS Code, select the repository interpreter at `.venv/bin/python` (Windows:
`.venv\Scripts\python.exe`) so the editor and terminal use the same packages.

If installation fails while linking `zstandard` against the macOS 27.0 SDK,
retry with an installed valid SDK. On the current setup:
```bash
SDKROOT=/Library/Developer/CommandLineTools/SDKs/MacOSX26.5.sdk \
  python -m pip install -r class2/requirements.txt
```
This sets `SDKROOT` only for that install command.

## What to run (in deck order)
| File | What it shows | Run (from the `class2` directory) |
|------|---------------|-----|
| `scraper.py` | Class 1 helper: URL -> page text | `python scraper.py` |
| `summarizer_langchain.py` | Block 10 — summarizer rebuilt in LangChain (prompt \| model \| parser) | `python summarizer_langchain.py` |
| `memory_demo.py` | Block 10 — memory with history typed by hand | `python memory_demo.py` |
| `memory_chat.py` | Block 10 — memory that builds itself in a chat loop | `python memory_chat.py` |
| `agent.py` | Block 11 — your first tool-using agent | `python agent.py` |
| `app.py` | Block 12 — the agent with a Gradio chat UI + public link | `python app.py` |

## Notes
- All files use the cheap `gpt-4o-mini` model.
- `summarizer_langchain.py` imports `fetch_website_contents` from `scraper.py`,
  so keep them in the same folder.
- `app.py` imports `agent` from `agent.py` — same folder.
- Keep your OpenAI key out of source control.

## Stop a running app
Press `Ctrl + C` in the terminal.
