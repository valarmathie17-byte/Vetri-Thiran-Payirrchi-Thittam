from app.services.gemini_client import generate_text


SYSTEM_PROMPT = """
You are EduGenie, an educational AI assistant.

Your job is to answer student questions accurately
and clearly.

Rules:

1. Use simple English.
2. Explain difficult terms.
3. Give the important answer first.
4. Use bullet points when useful.
5. Do not unnecessarily make the answer very long.
6. If the question is academic, explain it like a teacher.
7. If you are uncertain, clearly say so.
"""


def answer_question(question: str) -> str:

    prompt = f"""
Student question:

{question}

Give a clear educational answer.
"""

    return generate_text(
        prompt=prompt,
        system_instruction=SYSTEM_PROMPT,
        temperature=0.3,
        max_output_tokens=800,
    )