from fastapi import APIRouter, Depends
from app.api.deps import get_security_service
from app.models.dtos.user_dto import UserDto
from app.services.security_service import SecurityService

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
async def register(user: UserDto, security_service: SecurityService = Depends(get_security_service)):
    new_user = security_service.register(user)
    return new_user

@router.post("/login")
async def login(user: UserDto, security_service: SecurityService = Depends(get_security_service)):
    token = security_service.login(user)
    return token
