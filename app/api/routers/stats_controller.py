from fastapi import APIRouter, Request
from app.api.deps import get_security_service, get_stats_service
from app.services.security_service import SecurityService

router  = APIRouter(prefix='/api/v1/stats', tags=['Statistics'])

security_service: SecurityService = get_security_service()
stats_service = get_stats_service()

@router.get('/overview')
@security_service.authorize
async def get_stats_overview(request: Request):
    total_books = stats_service.count_all_books()
    average_price = stats_service.average_price()
    top_books = stats_service.top_rated_books()
    histogram = stats_service.rating_histogram()
    
    return {
        "total_books": total_books,
        "average_price": average_price,
        "top_rated_books": top_books,
        "histogram": histogram
    }

@router.get('/categories')
@security_service.authorize
async def get_categories_stats(request: Request):
    avg_price_by_category = stats_service.avg_price_by_category()
    book_by_category = stats_service.book_amount_by_category()
    
    return {
        "average_price_by_category": avg_price_by_category,
        "book_amount_by_category": book_by_category
    }

@router.get('/top-rated/{n}')
@security_service.authorize
async def get_top_rated_books(request: Request, n: int):
    top_books = stats_service.top_rated_books(n)
    return {
        "top_rated_books": top_books
    }