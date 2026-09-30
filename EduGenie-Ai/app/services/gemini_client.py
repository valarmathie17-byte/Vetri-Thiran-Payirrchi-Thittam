import json
import time
from typing import Optional

from google import genai
from google.genai import types

from app.config import get_settings


def get_client():

    settings = get_settings()

    if not settings.gemini_api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. "
            "Please add your Gemini API key to the .env file."
        )

    return genai.Client(
        api_key=settings.gemini_api_key
    )


def _generate_content_with_retry(
    client,
    model,
    contents,
    config,
    retries: int = 3,
):
    last_error = None

    for attempt in range(retries):

        try:
            return client.models.generate_content(
                model=model,
                contents=contents,
                config=config,
            )

        except Exception as exc:

            last_error = exc

            error_text = str(exc).upper()

            # Do NOT retry quota errors.
            # Retrying 429 will not increase the quota.
            if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
                raise RuntimeError(
                    "Gemini API quota has been exhausted. "
                    "Please try again after the quota resets."
                )

            # Retry temporary server errors only.
            if (
                "503" in error_text
                or "UNAVAILABLE" in error_text
            ):

                if attempt < retries - 1:
                    wait_time = 2 ** attempt

                    print(
                        f"Gemini temporarily unavailable. "
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)
                    continue

            raise

    raise last_error


def _demo_text(prompt: str) -> str:
    """
    Temporary demo response used when DEMO_MODE=true.
    This prevents Gemini API calls while testing the application.
    """

    prompt_lower = prompt.lower()

    if "pythagoras" in prompt_lower:
        return (
            "The Pythagoras Theorem is used in a right-angled triangle. "
            "It states that the square of the longest side equals the sum "
            "of the squares of the other two sides.\n\n"
            "Formula: a² + b² = c²"
        )

    if "largest ocean" in prompt_lower:
        return (
            "The Pacific Ocean is the largest ocean on Earth. "
            "It covers a larger area than the Atlantic, Indian, "
            "Southern and Arctic Oceans."
        )

    return (
        "This is a Demo Mode response from EduGenie.\n\n"
        "Gemini API is temporarily unavailable because the current "
        "API quota has been exhausted.\n\n"
        "Your EduGenie application is working, and real Gemini "
        "responses can be enabled again by changing DEMO_MODE=false "
        "after the API quota becomes available."
    )


def generate_text(
    prompt: str,
    system_instruction: Optional[str] = None,
    temperature: float = 0.4,
    max_output_tokens: int = 1000,
) -> str:

    settings = get_settings()

    # DEMO MODE
    if settings.demo_mode:
        print("EduGenie DEMO_MODE is active. Gemini API call skipped.")
        return _demo_text(prompt)

    # REAL GEMINI MODE
    client = get_client()

    config = types.GenerateContentConfig(
        temperature=temperature,
        max_output_tokens=max_output_tokens,
    )

    if system_instruction:
        config.system_instruction = system_instruction

    response = _generate_content_with_retry(
        client=client,
        model=settings.gemini_model,
        contents=prompt,
        config=config,
    )

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return response.text.strip()


def generate_json(
    prompt: str,
    system_instruction: Optional[str] = None,
    temperature: float = 0.3,
    max_output_tokens: int = 1500,
):

    settings = get_settings()

    # DEMO MODE
    if settings.demo_mode:
        print("EduGenie DEMO_MODE is active. Gemini JSON API call skipped.")

        return {
            "demo": True,
            "message": (
                "Demo Mode is active. Gemini API quota is currently "
                "exhausted. Real AI-generated JSON will be available "
                "when DEMO_MODE is set to false."
            )
        }

    # REAL GEMINI MODE
    client = get_client()

    config = types.GenerateContentConfig(
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        response_mime_type="application/json",
    )

    if system_instruction:
        config.system_instruction = system_instruction

    response = _generate_content_with_retry(
        client=client,
        model=settings.gemini_model,
        contents=prompt,
        config=config,
    )

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    text = response.text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    try:
        return json.loads(text)

    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"Gemini returned invalid JSON: {exc}"
        )