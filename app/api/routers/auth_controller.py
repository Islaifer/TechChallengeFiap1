from fastapi import APIRouter
from app.api.deps import get_security_service
from app.models.dtos.user_dto import UserDto
from app.services.security_service import SecurityService

router = APIRouter(prefix="/auth", tags=["Auth"])

security_service: SecurityService = get_security_service()

@router.post("/register")
async def register(user: UserDto):
    new_user = security_service.register(user)
    return new_user

@router.post("/login")
async def login(user: UserDto):
    token = security_service.login(user)
    return token
