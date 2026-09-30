from typing import Literal

from pydantic import BaseModel, Field


class QARequest(BaseModel):

    question: str = Field(
        ...,
        min_length=2,
        max_length=5000
    )


class ExplainRequest(BaseModel):

    topic: str = Field(
        ...,
        min_length=2,
        max_length=3000
    )

    level: Literal[
        "beginner",
        "intermediate",
        "advanced"
    ] = "beginner"


class QuizRequest(BaseModel):

    text: str = Field(
        ...,
        min_length=5,
        max_length=10000
    )

    level: Literal[
        "beginner",
        "intermediate",
        "advanced"
    ] = "beginner"

    count: int = Field(
        default=3,
        ge=1,
        le=10
    )


class SummaryRequest(BaseModel):

    text: str = Field(
        ...,
        min_length=20,
        max_length=20000
    )

    max_words: int = Field(
        default=150,
        ge=30,
        le=500
    )


class LearningPathRequest(BaseModel):

    topic: str = Field(
        ...,
        min_length=2,
        max_length=1000
    )

    level: Literal[
        "beginner",
        "intermediate",
        "advanced"
    ] = "beginner"

    weeks: int = Field(
        default=4,
        ge=1,
        le=52
    )