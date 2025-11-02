from fastapi import APIRouter, Request, Depends
from app.api.deps import get_security_service, get_books_service, get_none
from app.services.security_service import SecurityService
from app.services.books_service import BooksService
from app.models.dtos.user_dto import UserDto

router = APIRouter(prefix="/api/v1/books", tags=["Books"])

security_service: SecurityService = get_security_service()
books_service: BooksService = get_books_service()

@router.get("")
@security_service.authorize(target="user")
async def get_all_books(request: Request, user: UserDto = Depends(get_none)):
    return await books_service.get_all_books()

@router.get("/search")
@security_service.authorize(target="user")
async def get_all_books_filter(request: Request, title: str = None, category: str = None, user: UserDto = Depends(get_none)):
    return await books_service.filter_books(title, category)

@router.get("/{book_id}")
@security_service.authorize(target="user")
async def get_book(request: Request, book_id, user: UserDto = Depends(get_none)):
    return await books_service.get_by_id(book_id)
