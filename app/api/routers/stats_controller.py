from fastapi import APIRouter, Request, Depends
from app.api.deps import get_security_service, get_stats_service, get_none
from app.services.security_service import SecurityService
from app.models.dtos.user_dto import UserDto
from app.models.dtos.overview_dto import OverviewDto
from app.models.dtos.stats_dto import StatsDto
from app.models.dtos.top_rateds_dto import TopRatedsDto

router  = APIRouter(prefix='/api/v1/stats', tags=['Statistics'])

security_service: SecurityService = get_security_service()
stats_service = get_stats_service()

@router.get('/overview', response_model=OverviewDto, openapi_extra={"security": [{"Auth": []}]})
@security_service.authorize(target="user")
async def get_stats_overview(request: Request, user: UserDto = Depends(get_none)):
    """
    Rota que retorna um overview geral dos livros coletados.
    """
    total_books = await stats_service.count_all_books()
    average_price = await stats_service.average_price()
    top_books = await stats_service.top_rated_books()
    #histogram = await stats_service.rating_histogram()
    
    result = OverviewDto()
    result.total_books = total_books
    result.average_price = average_price
    result.top_books = top_books
    
    return result

@router.get('/categories', response_model=StatsDto, openapi_extra={"security": [{"Auth": []}]})
@security_service.authorize(target="user")
async def get_categories_stats(request: Request, user: UserDto = Depends(get_none)):
    """
    Rota que retorna estatísticas dos livros coletados por categoria
    """
    avg_price_by_category = await stats_service.avg_price_by_category()
    book_by_category = await stats_service.book_amount_by_category()
    
    result = StatsDto()
    result.avg_price_by_category = avg_price_by_category
    result.book_by_category = book_by_category
    
    return result

@router.get('/top-rated/{n}', response_model=TopRatedsDto, openapi_extra={"security": [{"Auth": []}]})
@security_service.authorize(target="user")
async def get_top_rated_books(request: Request, n: int, user: UserDto = Depends(get_none)):
    """
    Rota que retorna os top livros passados (a quantidade do top é definida pelo argumenmto passado no endpoint por path)
    """
    top_books = await stats_service.top_rated_books(n)
    
    result = TopRatedsDto()
    result.top_books = top_books
    
    return result