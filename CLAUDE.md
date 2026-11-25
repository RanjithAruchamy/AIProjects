# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

### Development
- `pip install -e .` - Install package in editable mode
- `black .` - Format code with Black
- `python -m ipykernel install --user` - Install IPython kernel

### Testing
- `pytest` - Run all tests
- `pytest -k <test_name>` - Run a single test
- `pytest --cov=ChatWithPDF` - Run tests with coverage

### Linting
- `flake8 .` - Run linter
- `bandit -r .` - Security linting

### Environment
- `.env` contains API keys and configuration - never commit this file
- Use virtual environments in `.venv`/`.venv313`

## Code Architecture

This project implements multi-model AI applications with these core components:

1. **ChatBot** - Core chatbot logic with natural language processing

2. **ChatWithPDF** - PDF document processing and analysis capabilities

3. **MultiModelComparision** - Framework for benchmarking different AI models

4. **MultipleToolCall** - System for invoking multiple tools/LLMs simultaneously

5. **Summarizer** - Text summarization and content extraction modules

6. **Gradio Interface** (.gradio) - Web UI for interacting with AI models

The architecture emphasizes modular design with clear separation between:
- Model interaction layers
- Document processing pipelines
- Comparative analysis frameworks
- User interface components

Key patterns include:
- Configuration management via .env
- Environment isolation with virtual environments
- Separation of concerns between model handling, processing, and UI