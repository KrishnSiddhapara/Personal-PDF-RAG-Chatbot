from fastapi import APIRouter
from backend.config import settings
from backend.models.schemas import HealthCheckResponse
from backend.utils.document_store import document_store

router = APIRouter(prefix="/api/health", tags=["Health"])

@router.get("", response_model=HealthCheckResponse)
async def health_check():
    """Returns application operational status and readiness."""
    docs = document_store.get_all()
    has_key = bool(settings.GEMINI_API_KEY and len(settings.GEMINI_API_KEY.strip()) > 0)
    
    return HealthCheckResponse(
        status="ok",
        version="1.0.0",
        document_count=len(docs),
        has_api_key=has_key
    )
