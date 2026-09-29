from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "LegalEase"
    app_version: str = "1.0.0"

    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"

    frontend_origin: str = "http://localhost:8501"
    max_document_chars: int = 12000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()