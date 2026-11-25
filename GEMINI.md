# GEMINI.md

This file provides project context and guidelines for Antigravity when working in the `AIProjects` repository.

## Environment & Security

- **Virtual Environments**: Use `.venv` or `.venv313` when running Python scripts, tests, or tools.
- **Secrets**: `.env` contains API keys and configuration. Never commit `.env` or expose its contents.

## Common Commands

### Development
- `pip install -e .` - Install package in editable mode
- `black .` - Format code with Black
- `python -m ipykernel install --user` - Install IPython kernel

### Testing
- `pytest` - Run all tests
- `pytest -k <test_name>` - Run a single test
- `pytest --cov=ChatWithPDF` - Run tests with coverage

### Linting & Security
- `flake8 .` - Run linter
- `bandit -r .` - Run security linting

## Project Structure & Architecture

This repository contains modular multi-model AI applications, each with its own entry point (`app.py`) and dependencies (`requirements.txt`):

- **`ChatBot/`**: Core chatbot logic, LangChain/agent workflows, web scraping, and memory-enabled chat (`app.py`, `agent.py`, `memory_chat.py`, `memory_demo.py`, `scraper.py`, `summarizer_langchain.py`).
- **`ChatWithPDF/`**: PDF document loading, processing, and Q&A (`app.py`, `pdf_chat.py`, `pdf_loader.py`).
- **`MultiModelComparision/`**: Framework for comparing and benchmarking different AI models (`app.py`).
- **`MultipleToolCall/`**: Multi-tool invocation experiments (`a.py`).
- **`Summarizer/`**: Web scraping and text summarization (`app.py`, `scraper.py`, `summarizer.py`).
- **`AIProjects/MultiFormatDocumentProcessor/`**: Multi-format document processing module.
- **`firstInteraction.py`**: Standalone initial interaction script at the repository root.
- **`.gradio/`**: Gradio web UI artifacts/configuration.

## Conventions

- Maintain separation of concerns between model interaction layers, document/data processing pipelines, and UI components (Gradio).
- Manage configuration and API keys through `.env` rather than hardcoding values.
- Keep existing module-level `requirements.txt` files updated when adding dependencies to a subproject.
