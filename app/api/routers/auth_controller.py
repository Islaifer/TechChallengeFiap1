from fastapi import APIRouter
from app.api.deps import get_security_service
from app.models.dtos.user_dto import UserDto
from app.services.security_service import SecurityService

router = APIRouter(prefix="/auth", tags=["Auth"])

security_service: SecurityService = get_security_service()

@router.post("/register", response_model=UserDto)
async def register(user: UserDto):
    """
    Rota feita para registro de usuários. Um usuário é necessário para utilizar as demais rotas do sistema

    Parameters
    ----------
    Usuário contendo nome, email e uma senha.

    Returns
    -------
    Retorno do usuário cadastrado, com a senha camuflada.

    """
    new_user = security_service.register(user)
    return new_user

@router.post("/login")
async def login(user: UserDto):
    """
    Rota para login. O login pode ser feito com o email ou o nome de usuario com a senha cadastrada.

    Parameters
    ----------
    Usuário contendo nome ou email e a senha.

    Returns
    -------
    Token em string

    """
    token = security_service.login(user)
    return token
