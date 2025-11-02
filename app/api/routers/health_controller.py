from fastapi import APIRouter
from datetime import datetime

router = APIRouter(prefix="/api/v1/health", tags=["Categories"])

@router.get("")
def health_check():
    return {
        "status": "UP",
        "timestamp": datetime.now().isoformat()
    }