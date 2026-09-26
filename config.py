from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "ComicCraft"
    app_env: str = "development"
    gemini_api_key: str = ""
    gemini_outline_model: str = "gemini-2.5-flash"
    gemini_story_model: str = "gemini-2.5-pro"
    hf_api_key: str = ""
    hf_provider: str = "auto"
    hf_image_model: str = "runwayml/stable-diffusion-v1-5"
    mock_ai: bool = True
    panel_count: int = 5
    image_width: int = 768
    image_height: int = 768
    image_steps: int = 20
    image_guidance: float = 7.5

    @property
    def project_root(self) -> Path:
        return Path(__file__).resolve().parent.parent

    @property
    def templates_dir(self) -> Path:
        return self.project_root / "templates"

    @property
    def static_dir(self) -> Path:
        return self.project_root / "static"


@lru_cache
def get_settings() -> Settings:
    return Settings()
