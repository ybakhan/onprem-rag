# OnPrem RAG

![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.128-009688?logo=fastapi&logoColor=white)
![LlamaIndex](https://img.shields.io/badge/LlamaIndex-RAG-f97316?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PC9zdmc+)
![ChromaDB](https://img.shields.io/badge/ChromaDB-vector_store-E25F27)
![HuggingFace](https://img.shields.io/badge/HuggingFace-embeddings-FFD21E?logo=huggingface&logoColor=black)
![LLM Guard](https://img.shields.io/badge/LLM_Guard-prompt_safety-8B5CF6)
![uv](https://img.shields.io/badge/uv-package_manager-DE5FE9)
![pytest](https://img.shields.io/badge/pytest-tested-0A9EDC?logo=pytest&logoColor=white)
![License: MIT](https://img.shields.io/badge/license-MIT-22c55e)

A fully on-premises Retrieval-Augmented Generation (RAG) service with an OpenAI-compatible API. Index PDF documents into a local vector store and query them through a chat completion endpoint — no data leaves your infrastructure.

## Features

- **OpenAI-compatible API** — drop-in replacement for `/v1/chat/completions` and `/v1/models`
- **PDF ingestion pipeline** — extracts, chunks, and embeds PDF content into ChromaDB
- **Multilingual** — Arabic and English support (switchable via `CHAT_COMPLETION_LANG`)
- **Prompt safety** — built-in LLM Guard scanning for token limits, invisible text, toxicity, and prompt injection
- **Flexible inference** — connect to a remote TGI server or run a model locally
- **Stable chunk IDs** — content-hashed document chunks for idempotent re-indexing

## Stack

| Component | Library |
|---|---|
| API framework | FastAPI |
| RAG / indexing | LlamaIndex |
| Vector store | ChromaDB |
| Embeddings | HuggingFace (`AraGemma-Embedding-300m`) |
| PDF parsing | PyMuPDF4LLM |
| Prompt safety | LLM Guard |
| Default LLM | `silma-ai/SILMA-Kashif-2B-Instruct-v1.0` (via TGI) |

## Setup

**1. Install [UV](https://docs.astral.sh/uv/)**

**2. Install dependencies**

```bash
uv sync --python 3.13
```

**3. Authenticate with Hugging Face** (required to download embedding models)

```bash
# Create a token at https://huggingface.co/settings/tokens
huggingface-cli login
```

**4. Configure environment**

Copy and edit the example below, or create a `.env` file:

```bash
# Required — path to your HuggingFace model cache
EMBEDDING_MODEL_DIR=~/.cache/huggingface/hub

# Optional overrides (defaults shown)
CHAT_COMPLETION_HOST=silma-kashif-2b-rag
CHAT_COMPLETION_PORT=9091
CHAT_COMPLETION_LANG=en          # "en" or "ar"
CHAT_COMPLETION_LOCAL=false      # true = run model in-process
DEVICE=cpu                       # "cpu" or "cuda"
VECTOR_DB_PATH=./storage/chromadb
```

See [src/app/config.py](src/app/config.py) for the full list of settings.

## Usage

### Index PDFs

```bash
CONTENT_DIR="./tests/docs/en" CONTENT_LANG="en" python ./scripts/index_pdf_dir.py
```

Point `CONTENT_DIR` at any folder of PDFs. Re-running is safe — chunks are identified by a content hash and won't be duplicated.

### Start the server

```bash
uv run fastapi run ./src/app/app.py --host localhost --port 8000
```

Or for development with auto-reload:

```bash
uv run python -m app.app
```

### Chat completion request

```bash
curl http://localhost:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{
    "messages": [{"role": "user", "content": "How do I register a child for school in Canada?"}],
    "max_tokens": 12000,
    "temperature": 0.5,
    "top_p": 0.95
  }'
```

### List available models

```bash
curl http://localhost:8000/v1/models
```

## API Reference

### `POST /v1/chat/completions`

| Field | Type | Default | Description |
|---|---|---|---|
| `messages` | array | required | Chat history. The last message is treated as the user query. |
| `max_tokens` | int | `12000` | Maximum tokens in the response |
| `temperature` | float | `0.5` | Sampling temperature |
| `top_p` | float | `0.95` | Nucleus sampling probability |

Responses follow the OpenAI chat completion schema including token usage.

### `GET /v1/models`

Returns the currently configured model as an OpenAI-compatible model list.

## Running Tests

```bash
source .venv/bin/activate
pytest ./tests -s
```

## Project Structure

```
src/app/
├── app.py          # FastAPI application entry point
├── config.py       # Pydantic settings (env-driven)
├── routes.py       # API route handlers
├── schemas.py      # Request / response models
├── middleware.py   # Request ID injection
├── errors.py       # Exception handlers
├── templates/
│   ├── chat_completion_en.jinja
│   └── chat_completion_ar.jinja
└── core/
    ├── indexer.py               # PDF → vector store pipeline
    ├── ingestion_pipeline.py
    ├── embedding_model.py
    ├── vector_store.py          # ChromaDB wrapper
    ├── document_store.py
    ├── query.py                 # RAG retrieval
    ├── chat_completion.py       # Remote TGI inference
    ├── chat_completion_local.py # Local inference
    ├── scanner.py               # LLM Guard prompt safety
    ├── prompt.py                # Prompt templates
    ├── common.py
    └── exceptions.py

scripts/
├── index_pdf_dir.py            # Batch PDF indexing
├── chat_completion_en.py       # English test client (direct)
├── chat_completion_ar.py       # Arabic test client (direct)
├── chat_completion_tgi_en.py   # English test client (TGI)
├── chat_completion_tgi_ar.py   # Arabic test client (TGI)
└── chat_completion_local_ar.py # Arabic test client (local inference)
```
