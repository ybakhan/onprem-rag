from llama_index.core.prompts import RichPromptTemplate


def generate_prompt(question, context):
    """Generate a prompt for the chat completion model with the question and context."""

    template_str = """
    Answer the following question using only the information provided in the context below.
    Do NOT use any outside knowledge.
    If the context does not contain the necessary information, respond with:
    "I'm sorry, but the provided context does not contain enough information to answer this question."


    Context:
    {{context}}


    Question:
    {{question}}


    Answer:
    """

    prompt_template = RichPromptTemplate(template_str=template_str)
    prompt = prompt_template.format(context=context, question=question)

    return prompt
