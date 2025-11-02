from fastapi import APIRouter
from datetime import datetime
from typing import Any

router = APIRouter(prefix="/api/v1/health", tags=["Categories"])

@router.get("")
def health_check() -> dict[str, Any]:
    """
    Rota que retorna o status da API.
    """
    return {
        "status": "UP",
        "timestamp": datetime.now().isoformat()
    }