from functools import lru_cache

from app.config import get_settings
from app.services.gemini_client import generate_text


@lru_cache(maxsize=1)
def load_local_model():

    settings = get_settings()

    try:

        from transformers import pipeline

        model = pipeline(
            "text2text-generation",
            model=settings.local_model_name,
            device=-1,
        )

        return model

    except Exception:
        return None


def local_explanation(
    topic: str,
    level: str
) -> str:

    model = load_local_model()

    if model is None:
        raise RuntimeError(
            "Local explanation model is not available."
        )

    prompt = f"""
Explain the following topic for a {level} student.

Topic:
{topic}

Use simple English.
Give:
1. Definition
2. Main points
3. Simple example
4. Short conclusion
"""

    result = model(
        prompt,
        max_new_tokens=get_settings().local_max_new_tokens,
        do_sample=False,
    )

    if not result:
        raise RuntimeError(
            "Local model returned no result."
        )

    return result[0]["generated_text"].strip()


def gemini_explanation(
    topic: str,
    level: str
) -> str:

    prompt = f"""
Explain this topic for a {level} student:

{topic}

Format the answer with:

Definition
Main Points
Simple Example
Conclusion

Use simple English.
"""

    return generate_text(
        prompt=prompt,
        system_instruction="""
You are an educational teacher.
Explain concepts clearly and simply.
""",
        temperature=0.3,
        max_output_tokens=900,
    )


def explain_topic(
    topic: str,
    level: str = "beginner"
) -> str:

    settings = get_settings()

    provider = settings.explanation_provider.lower()

    if provider == "local":

        try:
            return local_explanation(
                topic,
                level
            )

        except Exception:
            return gemini_explanation(
                topic,
                level
            )

    return gemini_explanation(
        topic,
        level
    )