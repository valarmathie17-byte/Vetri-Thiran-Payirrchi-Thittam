from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "EduGenie"
    environment: str = "development"

    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.8-flash"

    explanation_provider: str = "gemini"
    demo_mode: bool = False

    local_model_name: str = "MBZUAI/LaMini-Flan-T5-783M"
    local_max_new_tokens: int = 180

    request_timeout_seconds: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()