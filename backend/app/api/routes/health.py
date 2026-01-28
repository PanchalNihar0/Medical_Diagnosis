"""
Health check endpoints.
"""
from fastapi import APIRouter
from pydantic import BaseModel

from app.config import settings


router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    app_name: str
    version: str


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Check API health status.
    Returns application name and version.
    """
    return HealthResponse(
        status="healthy",
        app_name=settings.app_name,
        version=settings.app_version
    )
