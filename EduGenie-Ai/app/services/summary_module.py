from app.services.gemini_client import generate_text


def summarize_text(
    text: str,
    max_words: int = 150
) -> str:

    prompt = f"""
Summarize the following educational text.

Requirements:

- Maximum approximately {max_words} words.
- Keep the important information.
- Remove repetition.
- Use simple English.
- Do not add information that is not in the original text.

Text:

{text}
"""

    return generate_text(
        prompt=prompt,
        system_instruction="""
You are EduGenie's summarization assistant.
Create concise and accurate educational summaries.
""",
        temperature=0.2,
        max_output_tokens=700,
    )