import json
import logging
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from app.core.query import query
from app.core.prompt import generate_prompt
from app.config import settings
from app.core.scanner import is_prompt_safe

logger = logging.getLogger(__name__)

if settings.DEVICE == "cuda" and torch.cuda.is_bf16_supported():
    DTYPE = torch.bfloat16  # ← best on modern NVIDIA (Ampere+)
elif settings.DEVICE in ("cuda", "mps"):
    DTYPE = torch.float16  # ← very good on MPS, acceptable fallback on old CUDA
else:
    DTYPE = torch.float32  # ← CPU default (safe & precise)

model = AutoModelForCausalLM.from_pretrained(settings.CHAT_COMPLETION_MODEL_ID, torch_dtype=DTYPE)
tokenizer = AutoTokenizer.from_pretrained(settings.CHAT_COMPLETION_MODEL_ID)

pipe = pipeline(
    task="text-generation",
    model=model,
    tokenizer=tokenizer,
    device=settings.DEVICE,
)


def chat_completion_local(question, lang, previous_messages=None, **kwargs):
    """
    Generate a chat completion response using retrieved context and local chat completion model.
    """

    is_prompt_safe(question)
    context = query(question, lang)
    prompt = generate_prompt(question, context, lang)

    if previous_messages is None:
        previous_messages = []

    text_inputs = previous_messages + [
        {
            "role": "user",
            "content": prompt,
        },
    ]
    logger.debug("Chat completion local request\n%s", json.dumps(text_inputs, indent=2))

    generate_kwargs = {
        "max_new_tokens": kwargs.get("max_tokens", settings.CHAT_COMPLETION_MAX_TOKENS),
        "temperature": kwargs.get("temperature", settings.CHAT_COMPLETION_TEMPERATURE),
        "top_p": kwargs.get("top_p", settings.CHAT_COMPLETION_TOP_P),
        #"top_k": kwargs.get("top_k", settings.CHAT_COMPLETION_TOP_K),  # OpenAI spec doesn't require top_k but pytorch pipeline supports it
        "do_sample": True,
    }

    prompt_text = tokenizer.apply_chat_template(text_inputs, tokenize=False, add_generation_prompt=True)
    prompt_tokens = len(tokenizer(prompt_text)["input_ids"])

    outputs = pipe(
        text_inputs=text_inputs, **generate_kwargs
    )
    logger.debug("Chat completion response\n%s", json.dumps(outputs, indent=2))

    answer = outputs[0]["generated_text"][-1]["content"].strip()
    completion_tokens = len(tokenizer(answer)["input_ids"])

    return answer, prompt_tokens, completion_tokens
