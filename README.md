### Distant Light RAG Application

1. Install [UV](https://docs.astral.sh/uv/)
2. Run `uv sync`
3. Create a Hugging Face [access token](https://huggingface.co/settings/tokens)
4. Run `huggingface-cli login` and set access token
5. Set environment variable `EMBEDDING_MODEL_DIR` to your Hugging Face cache `~/.cache/huggingface/hub`
6. Run tests
   - `source .venv/bin/activate`
   - `pytest ./tests -s`
