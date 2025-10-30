from app.services.redis_service import RedisService

class BooksService:
    def __init__(self, redis_service: RedisService):
        self.redis_service = redis_service
        
    def get_all_books(self):
        books = self.redis_service.get_all("books")
        return books
    
    def get_by_id(self, book_id):
        book = self.redis_service.get_value("books", book_id)
        return book
    
    def filter_books(self, title: str, category: str):
        all_books = self.get_all_books()
        result = [book for book in all_books if (title is None or title in book['title']) and (category is None or category in book['category'])]
        return result
    
    def get_all_categories(self):
        all_categories = self.redis_service.get_all("category_list")
        return all_categories