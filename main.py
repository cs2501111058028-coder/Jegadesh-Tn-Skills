from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import get_settings
from app.routes import router
from app.services.comic_service import ComicService


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()

    app.state.settings = settings
    app.state.templates = Jinja2Templates(
        directory=str(settings.templates_dir)
    )
    app.state.comic_service = ComicService(settings)

    yield


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="AI-powered comic generation application",
    version="1.0.0",
    lifespan=lifespan,
)

app.mount(
    "/static",
    StaticFiles(directory=str(settings.static_dir)),
    name="static",
)

app.include_router(router)