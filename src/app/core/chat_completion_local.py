import json
import logging
import torch
from transformers import pipeline
from app.core.query import query
from app.core.prompt import generate_prompt
from app.config import settings

logger = logging.getLogger(__name__)

if settings.DEVICE == "cuda" and torch.cuda.is_bf16_supported():
    DTYPE = torch.bfloat16  # ← best on modern NVIDIA (Ampere+)
elif settings.DEVICE in ("cuda", "mps"):
    DTYPE = torch.float16  # ← very good on MPS, acceptable fallback on old CUDA
else:
    DTYPE = torch.float32  # ← CPU default (safe & precise)

pipe = pipeline(
    task="text-generation",
    model=settings.CHAT_COMPLETION_MODEL_ID,
    device=settings.DEVICE,
    dtype=DTYPE,
)


def chat_completion_local(question, lang):
    """
    Generate a chat completion response using retrieved context and local chat completion model.
    """
    context = query(question)
    prompt = generate_prompt(question, context, lang)

    text_inputs = [
        {
            "role": "user",
            "content": prompt,
        },
    ]
    logger.debug("Chat completion local request\n%s", json.dumps(text_inputs, indent=2))

    outputs = pipe(
        text_inputs=text_inputs, max_new_tokens=settings.CHAT_COMPLETION_MAX_TOKENS
    )
    logger.debug("Chat completion response\n%s", json.dumps(outputs, indent=2))

    answer = outputs[0]["generated_text"][-1]["content"].strip()
    return answer
