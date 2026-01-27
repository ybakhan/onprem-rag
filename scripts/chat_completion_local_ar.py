# pylint: skip-file
import json
from app.core.chat_completion_local import chat_completion_local

SAMPLE_QUESTION = "كيف يمكن الوصول إلى المكتبات العامة في كندا؟"  # "How to access public libraries in Canada?"

response = chat_completion_local(SAMPLE_QUESTION, "ar")

# save to file for better Arabic text display
with open("response.json", "w", encoding="utf-8") as f:
    json.dump(response, f, indent=2, ensure_ascii=False)
