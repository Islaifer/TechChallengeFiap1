from fastapi import APIRouter, Request, Depends
from app.models.dtos.user_dto import UserDto
from app.api.deps import get_security_service, get_user_service, get_none
from app.services.security_service import SecurityService
from app.services.user_service import UserService

router = APIRouter(prefix="/user", tags=["Users"])

security_service: SecurityService = get_security_service()
user_service: UserService = get_user_service()

@router.get("", response_model=UserDto, openapi_extra={"security": [{"Auth": []}]})
@security_service.authorize(target="user")
async def get_self_user(request: Request, user: UserDto = Depends(get_none)):
    """
    Rota que retorna os dados do usuário através do token.
    """
    return user

@router.put("", response_model=UserDto, openapi_extra={"security": [{"Auth": []}]})
@security_service.authorize(target="user")
async def update_self_user(request: Request, user_updated: UserDto, user: UserDto = Depends(get_none)):
    """
    Rota que atualiza os dados do usuário.
    """
    return user_service.update_user(user.id, user_updated)