from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Korea Economic Stats AI Agent"

    OPENAI_API_KEY: str = ""
    ECOS_API_KEY: str = ""

    CHAT_MODEL: str = "gpt-5-mini"
    EMBEDDING_MODEL: str = "text-embedding-3-small"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
        frozen=True,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
