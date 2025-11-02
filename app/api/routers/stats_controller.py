from fastapi import APIRouter, Request, Depends
from app.api.deps import get_security_service, get_stats_service, get_none
from app.services.security_service import SecurityService
from app.models.dtos.user_dto import UserDto

router  = APIRouter(prefix='/api/v1/stats', tags=['Statistics'])

security_service: SecurityService = get_security_service()
stats_service = get_stats_service()

@router.get('/overview')
@security_service.authorize(target="user")
async def get_stats_overview(request: Request, user: UserDto = Depends(get_none)):
    total_books = await stats_service.count_all_books()
    average_price = await stats_service.average_price()
    top_books = await stats_service.top_rated_books()
    #histogram = await stats_service.rating_histogram()
    
    return {
        "total_books": total_books,
        "average_price": average_price,
        "top_rated_books": top_books,
        #"histogram": histogram
    }

@router.get('/categories')
@security_service.authorize(target="user")
async def get_categories_stats(request: Request, user: UserDto = Depends(get_none)):
    avg_price_by_category = await stats_service.avg_price_by_category()
    book_by_category = await stats_service.book_amount_by_category()
    
    return {
        "average_price_by_category": avg_price_by_category,
        "book_amount_by_category": book_by_category
    }

@router.get('/top-rated/{n}')
@security_service.authorize(target="user")
async def get_top_rated_books(request: Request, n: int, user: UserDto = Depends(get_none)):
    top_books = await stats_service.top_rated_books(n)
    return {
        "top_rated_books": top_books
    }