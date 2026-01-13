from pathlib import Path
from llama_index.core.prompts import RichPromptTemplate


def generate_prompt(question, context, lang):
    """Generate a prompt for the chat completion model with the question and context."""

    template_path = (
        Path(__file__).parent.parent / "templates" / f"chat_completion_{lang}.jinja"
    )
    template_str = template_path.read_text()
    prompt_template = RichPromptTemplate(template_str=template_str)
    prompt = (
        prompt_template.format(context=context, question=question) + "\n"
    )  # add trailing new line which gets removed by format

    return prompt
