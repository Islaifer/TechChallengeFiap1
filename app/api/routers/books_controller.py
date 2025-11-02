from fastapi import APIRouter, Request, Depends
from app.api.deps import get_security_service, get_books_service, get_none
from app.services.security_service import SecurityService
from app.services.books_service import BooksService
from app.models.dtos.user_dto import UserDto
from app.models.dtos.book_dto import BookDto

router = APIRouter(prefix="/api/v1/books", tags=["Books"])

security_service: SecurityService = get_security_service()
books_service: BooksService = get_books_service()

@router.get("", response_model=list[BookDto], openapi_extra={"security": [{"Auth": []}]})
@security_service.authorize(target="user")
async def get_all_books(request: Request, user: UserDto = Depends(get_none)):
    """
    Rota que retorna todos os livros.
    """
    return await books_service.get_all_books()

@router.get("/search", response_model=list[BookDto], openapi_extra={"security": [{"Auth": []}]})
@security_service.authorize(target="user")
async def get_all_books_filter(request: Request, title: str = None, category: str = None, user: UserDto = Depends(get_none)):
    """
    Rota que filtra os livros pelo nome e/ou categoria
    """
    return await books_service.filter_books(title, category)

@router.get("/{book_id}", response_model=BookDto, openapi_extra={"security": [{"Auth": []}]})
@security_service.authorize(target="user")
async def get_book(request: Request, book_id, user: UserDto = Depends(get_none)):
    """
    Rota que pega um livro especifico pelo id
    """
    return await books_service.get_by_id(book_id)
