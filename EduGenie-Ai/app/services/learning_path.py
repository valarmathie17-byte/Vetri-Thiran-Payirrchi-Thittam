from app.services.gemini_client import generate_json


def get_learning_recommendations(
    topic: str,
    level: str = "beginner",
    weeks: int = 4
):

    prompt = f"""
Create a personalized learning path.

Topic:
{topic}

Current level:
{level}

Duration:
{weeks} weeks

Create a progression from beginner to advanced
where appropriate.

For each week include:

- week
- title
- topics
- activities
- resources

Resources can include:
- videos
- articles
- books
- practice activities

Return ONLY valid JSON.

Format:

[
  {{
    "week": 1,
    "title": "Introduction",
    "topics": ["Topic 1", "Topic 2"],
    "activities": [
      "Activity 1",
      "Activity 2"
    ],
    "resources": [
      "Resource 1",
      "Resource 2"
    ]
  }}
]
"""

    result = generate_json(
        prompt=prompt,
        system_instruction="""
You are EduGenie's personalized learning planner.

Create practical and educational learning plans.
Keep the progression logical.
Return valid JSON only.
""",
        temperature=0.4,
        max_output_tokens=2500,
    )

    if not isinstance(result, list):
        raise RuntimeError(
            "Learning path response is not a list."
        )

    return result[:weeks]