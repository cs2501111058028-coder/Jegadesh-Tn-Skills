from typing import List

from pydantic import BaseModel, ConfigDict, Field


class PromptRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    story_prompt: str = Field(..., min_length=10, max_length=2000)
    character_name: str = Field(..., min_length=1, max_length=80)
    setting: str = Field(default="enchanted forest", max_length=120)
    tone: str = Field(default="dramatic", max_length=80)
    art_style: str = Field(default="comic book", max_length=80)


class ComicPanel(BaseModel):
    panel_number: int
    title: str
    description: str
    image_url: str


class ComicLayout(BaseModel):
    comic_id: str
    title: str
    summary: str
    panels: List[ComicPanel]
