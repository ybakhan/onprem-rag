import json
import deepl
from deepl.api_data import ModelType

auth_key = "b5cdf9a7-b09d-4ba2-89da-24ba4017fc28"
deepl_client = deepl.DeepLClient(auth_key)

def to_arabic(text):
    return translate(text, "EN", "AR")

def to_english(text):
    return translate(text, "AR", "EN-US")

def translate(text, source_lang, target_lang):
    result = deepl_client.translate_text(
        text=text, 
        source_lang=source_lang,                               
        target_lang=target_lang,
        model_type=ModelType.QUALITY_OPTIMIZED,
    )
    return result
