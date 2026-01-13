# pylint: skip-file
import json
import requests

prompt = """Answer the following question using only the information provided in the context below.
Do NOT use any outside knowledge.
If the context does not contain the necessary information, respond with:
"I'm sorry, but the provided context does not contain enough information to answer this question."

Context:
The company was founded in Vancouver in early 2018 by Sarah Chen and Miguel Ortiz. 
Initial funding came from Y Combinator's Summer 2018 batch.
The main product is a cloud-based platform for automated compliance reporting in fintech.
As of Q3 2025, the company has 47 employees and serves 120+ financial institutions across Canada and the United States.

Question: When was ComplyFlow incorporated and in which city and by whom?

Answer:"""

payload = {
    "model": "silma-ai/SILMA-Kashif-2B-Instruct-v1.0",
    "messages": [
        {
            "role": "user",
            "content": prompt,
        }
    ],
}

print("=" * 50)
print(json.dumps(payload, indent=2))

response = requests.post(
    "http://silma-kashif-2b-rag:9091/v1/chat/completions",
    headers={"Content-Type": "application/json"},
    json=payload,
)

print("=" * 50)
print(json.dumps(response.json(), indent=2))
