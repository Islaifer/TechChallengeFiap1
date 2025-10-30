from app.core.config.redis_settings import RedisConnection
from redis_service import RedisService

class StatsisticsService:
    def __init__(self, data_source, redis_service = RedisService()):
        self.data_source = data_source
        self.redis_service = redis_service

    def count_all_books(self):
        """Retorna o total de livros na fonte de dados."""

        books = self.redis.service.get_all("books")

        if books is not None:
            return print(f'O total de livros é: {len(books)}')
        else:
            return None
    