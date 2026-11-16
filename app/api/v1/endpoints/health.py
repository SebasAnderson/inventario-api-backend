from fastapi import APIRouter
from typing import Dict

router = APIRouter()


@router.get("/health", summary="Health check endpoint", tags=["Health"])
def health_check() -> Dict[str, str]:
    """
    Endpoint de verificación de estado de la API.
    Retorna estado operativo y versión actual.
    """
    return {
        "status": "healthy",
        "service": "Comic & Manga Inventory API",
        "version": "0.1.0"
    }
