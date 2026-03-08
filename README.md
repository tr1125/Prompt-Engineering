# CLIByAI

A Gradio-based web app that translates natural-language instructions into Windows CLI commands using Google Gemini AI.

## What it does

Type a plain-English (or Hebrew) description of what you want to do — CLIByAI returns the exact, ready-to-run Windows command. The model is guided by a carefully engineered system prompt that enforces security rules, blocks dangerous commands, and keeps responses focused on CLI output only.

## Project structure

```
CLIByAI/
├── main.py                  # Entry point — launches the Gradio app
├── gradio_app.py            # Gradio UI and request handler
├── llm_client.py            # Google GenAI client (Gemini 2.5 Flash Lite)
├── pyproject.toml           # Project metadata and dependencies
├── prompts/
│   └── prompt3.md           # System prompt used by the LLM
├── utils/
│   └── validate_command.py  # Static safety validator for generated commands
├── sandbox/
│   └── runner.py            # Dry-run sandbox executor
└── logs/
    └── genai_raw.txt        # Raw LLM responses (debug log)
```

## Requirements

- Python 3.12+
- A valid `GOOGLE_API_KEY` for Google Gemini

## Installation

```bash
pip install -e .
```

Or install dependencies directly:

```bash
pip install gradio google-genai python-dotenv
```

## Configuration

Create a `.env` file in the project root (or inside `CLIByAI/`) with your API key:

```
GOOGLE_API_KEY=your_key_here
```

## Running

```bash
python -m CLIByAI.main
```

Then open the Gradio interface in your browser and type your instruction, for example:

> *List all files in the current directory, including hidden ones*

The app returns the matching CLI command (`dir /a`).

## Safety

The system prompt contains an **Iron Rule** — commands that could cause irreversible damage (formatting drives, shutting down the system, deleting entire directories, modifying security settings) are blocked. The LLM returns `SECURITY_RISK` for such requests.

Requests that contain no CLI action at all (e.g. "what time is it") return `NOT_A_CLI_COMMAND`.

An additional static validator (`utils/validate_command.py`) tokenizes every generated command and checks it against a list of forbidden programs and risky flags before execution.

## Tech stack

| Layer | Technology |
|---|---|
| UI | [Gradio](https://www.gradio.app/) |
| LLM | Google Gemini 2.5 Flash Lite via `google-genai` |
| Prompt engineering | Markdown system prompt (`prompts/prompt3.md`) |
| Validation | Custom Python tokenizer |
