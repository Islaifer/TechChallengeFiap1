from fastapi import APIRouter, Request
from app.api.deps import get_security_service, get_books_service
from app.services.security_service import SecurityService
from app.services.books_service import BooksService

router = APIRouter(prefix="/api/v1/books", tags=["Books"])

security_service: SecurityService = get_security_service()
books_service: BooksService = get_books_service()

@router.get("")
@security_service.authorize
async def get_all_books(request: Request):
    return books_service.get_all_books()

@router.get("/{book_id}")
@security_service.authorize
async def get_book(request: Request, book_id):
    return books_service.get_by_id(book_id)