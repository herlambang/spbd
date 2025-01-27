from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_PATH = Path(__file__).parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    _env: str = "dev"
    db_url: str
    storage_path: Path = PROJECT_PATH / "storage"
    audio_formats: list[str] = ["m4a"]


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
