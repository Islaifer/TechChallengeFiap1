from fastapi import APIRouter, Request, Depends
from app.api.deps import get_security_service, get_books_service, get_none
from app.services.security_service import SecurityService
from app.services.books_service import BooksService
from app.models.dtos.user_dto import UserDto

router = APIRouter(prefix="/api/v1/categories", tags=["Categories"])

security_service: SecurityService = get_security_service()
books_service: BooksService = get_books_service()

@router.get("")
@security_service.authorize(target="user")
async def get_all_categories(request: Request, user: UserDto = Depends(get_none)):
    return await books_service.get_all_categories()