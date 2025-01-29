from functools import lru_cache
from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_PATH = Path(__file__).parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Sourced from env vars
    _env: str = "dev"
    db_url: str
    storage_dir: Path = PROJECT_PATH / "storage"

    # Static settings
    audio_target_format: str = "wav"
    audio_target_ext: str = ".wav"
    audio_formats: list[str] = ["m4a", "mp3", "wav"]

    @computed_field
    @property
    def audio_dir(self) -> Path:
        return self.storage_dir / "audio"

    @computed_field
    @property
    def cached_dir(self) -> Path:
        return self.storage_dir / "cached"


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
