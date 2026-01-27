import json
from app.core.chat_completion import chat_completion

SAMPLE_QUESTION = "ما هي شركات تقديم خدمات التوطين؟"

response = chat_completion(SAMPLE_QUESTION, "ar")

# save to file for better Arabic text display
with open("response.json", "w", encoding="utf-8") as f:
    json.dump(response, f, indent=2, ensure_ascii=False)
