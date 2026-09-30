from app.services.gemini_client import generate_json


def generate_quiz(
    text: str,
    level: str = "beginner",
    count: int = 3
):

    prompt = f"""
Create {count} multiple-choice questions from the
following educational text.

Difficulty level:
{level}

For every question provide:

- question
- exactly 4 options
- correct answer
- short explanation

Return ONLY valid JSON.

Required format:

[
  {{
    "question": "Question here",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "answer": "Correct option",
    "explanation": "Short explanation"
  }}
]

Text:

{text}
"""

    result = generate_json(
        prompt=prompt,
        system_instruction="""
You are an educational quiz generator.

Generate questions only from the supplied text.
Do not invent unrelated information.

Always return valid JSON.
""",
        temperature=0.4,
        max_output_tokens=1800,
    )

    if not isinstance(result, list):
        raise RuntimeError(
            "Quiz response is not a list."
        )

    cleaned_quiz = []

    for item in result[:count]:

        if not isinstance(item, dict):
            continue

        question = str(
            item.get("question", "")
        ).strip()

        options = item.get(
            "options",
            []
        )

        answer = str(
            item.get("answer", "")
        ).strip()

        explanation = str(
            item.get("explanation", "")
        ).strip()

        if not question:
            continue

        if not isinstance(options, list):
            continue

        options = [
            str(option).strip()
            for option in options
            if str(option).strip()
        ]

        if len(options) != 4:
            continue

        # Support answer as an index
        if answer.isdigit():

            index = int(answer)

            if 0 <= index < len(options):
                answer = options[index]

            elif 1 <= index <= len(options):
                answer = options[index - 1]

        # If answer does not match exactly,
        # try case-insensitive matching.
        matched_answer = None

        for option in options:

            if option.lower() == answer.lower():
                matched_answer = option
                break

        if matched_answer:
            answer = matched_answer

        if answer not in options:
            continue

        cleaned_quiz.append(
            {
                "question": question,
                "options": options,
                "answer": answer,
                "explanation": explanation,
            }
        )

    if not cleaned_quiz:
        raise RuntimeError(
            "Could not create a valid quiz."
        )

    return cleaned_quiz