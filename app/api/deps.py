from app.services.security_service import SecurityService
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.services.redis_service import RedisService
from app.services.books_service import BooksService
from app.services.statistics_service import StatsisticsService
from app.services.extract import ExtractService

user_repository = UserRepository()
redis_service = RedisService()

security_service = SecurityService(user_repository)
extract_service = ExtractService(redis_service)
user_service = UserService(user_repository)
books_service = BooksService(redis_service, extract_service)
statistics_service = StatsisticsService(redis_service)

def get_security_service():
    return security_service

def get_user_service():
    return user_service

def get_books_service():
    return books_service

def get_stats_service():
    return statistics_service

def get_extractor():
    return extract_service

def get_none():
    return None