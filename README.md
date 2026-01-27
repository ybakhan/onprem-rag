### Distant Light RAG Application

1. Install [UV](https://docs.astral.sh/uv/)

2. Run `uv sync`

3. Create a Hugging Face [access token](https://huggingface.co/settings/tokens)

4. Run `huggingface-cli login` and set access token

5. Set environment variable `EMBEDDING_MODEL_DIR` to your Hugging Face cache `~/.cache/huggingface/hub`

6. Run tests

   ```bash
   source .venv/bin/activate
   pytest ./tests -s
   ```

7. Index PDF content

   ```bash
   CONTENT_DIR="./tests/docs/en" CONTENT_LANG="en" python ./scripts/index_pdf_dir.py
   ```

8. Run chat completion server

   ```bash
   uv run fastapi run ./src/app/app.py --host localhost --port 8000
   ```

9. POST chat completion request
   ```bash
   curl --location 'http://localhost:8000/v1/chat/completions' \
      --header 'Content-Type: application/json' \
      --data '{
         "max_tokens": 12000,
         "temperature": 0.5,
         "top_p": 0.95,
         "lang": "en",
         "messages": [
            {
                  "role": "user",
                  "content": "How to register a child for school in Canada?"
            }
         ]
      }'
   ```
