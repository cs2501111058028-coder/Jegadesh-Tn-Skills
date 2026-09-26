from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import ValidationError

from app.config import Settings
from app.models import PromptRequest
from app.services.comic_service import ComicService


router = APIRouter()


def get_service(request: Request) -> ComicService:
    return request.app.state.comic_service


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return request.app.state.templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request},
    )


@router.post("/generate", response_class=HTMLResponse)
def generate(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...),
):
    try:
        payload = PromptRequest(
            story_prompt=story_prompt,
            character_name=character_name,
            setting=setting,
            tone=tone,
            art_style=art_style,
        )
        layout = get_service(request).generate(payload)
        return request.app.state.templates.TemplateResponse(
            request=request,
            name="comic_preview.html",
            context={
                "request": request,
                "layout": layout,
                "pdf_url": f"/download/{layout.comic_id}",
            },
        )
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=exc.errors()) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Comic generation failed: {exc}") from exc


@router.post("/generate-comic/json")
def generate_json(request: Request, payload: PromptRequest):
    try:
        layout = get_service(request).generate(payload)
        return {
            "comic_id": layout.comic_id,
            "message": "Comic generated successfully.",
            "pdf_url": f"/download/{layout.comic_id}",
            "layout": layout.model_dump(),
        }
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Comic generation failed: {exc}") from exc


@router.get("/download/{comic_id}")
def download(comic_id: str, request: Request):
    path = get_service(request).get_pdf_path(comic_id)
    if not path:
        raise HTTPException(status_code=404, detail="Comic PDF not found.")

    return FileResponse(
        path=path,
        media_type="application/pdf",
        filename=f"comiccraft-{comic_id}.pdf",
    )


@router.get("/export-success", response_class=HTMLResponse)
def export_success(request: Request):
    return request.app.state.templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={"request": request},
    )


@router.post("/test-image")
def test_image(request: Request, prompt: str = Form(...)):
    try:
        service = get_service(request)
        image_url = service.images.generate_image(
            prompt=prompt,
            panel_number=0,
            title="image-test",
            comic_id="test",
        )
        return {"image_url": image_url}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Image generation failed: {exc}") from exc


@router.get("/health")
def health(request: Request):
    settings: Settings = request.app.state.settings
    return {
        "status": "ok",
        "app": settings.app_name,
        "environment": settings.app_env,
        "mock_ai": settings.mock_ai,
        "gemini_configured": bool(settings.gemini_api_key),
        "huggingface_configured": bool(settings.hf_api_key),
    }
