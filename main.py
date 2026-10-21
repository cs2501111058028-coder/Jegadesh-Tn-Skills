import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from google import genai

load_dotenv()

app = FastAPI(title="ComicCraft AI Comic Creator")

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY) if API_KEY else None


class StoryRequest(BaseModel):
    idea: str
    genre: str = "Fantasy"
    panels: int = 4


@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.post("/api/generate")
def generate_story(request: StoryRequest):
    if not client:
        raise HTTPException(
            status_code=500,
            detail="GEMINI_API_KEY is missing from the .env file."
        )

    idea = request.idea.strip()

    if not idea:
        raise HTTPException(
            status_code=400,
            detail="Please enter a story idea."
        )

    if len(idea) > 1500:
        raise HTTPException(
            status_code=400,
            detail="Please keep your story idea under 1500 characters."
        )

    if request.panels not in [4, 6, 8]:
        raise HTTPException(
            status_code=400,
            detail="Choose 4, 6, or 8 panels."
        )

    prompt = f"""
    You are ComicCraft, a creative comic story writer.

    Create a {request.panels}-panel comic story.
    Genre: {request.genre}
    User's story idea: {idea}

    Write in simple English.
    Make the story original, coherent, and suitable for students.

    For every panel, provide:
    Panel number:
    Scene description:
    Character dialogue:

    Include exactly {request.panels} panels.
    Return plain text with clear panel headings.
    """

    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )

        story = response.text

        if not story:
            raise HTTPException(
                status_code=502,
                detail="The AI returned an empty response."
            )

        return {
            "title": "Your ComicCraft Story",
            "genre": request.genre,
            "story": story
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=502,
            detail="AI generation failed. Check your API access and try again."
        )


app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)