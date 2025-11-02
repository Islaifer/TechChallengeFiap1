from app.services.redis_service import RedisService
from app.services.extract import ExtractService
from datetime import datetime, timedelta
import asyncio

class BooksService:
    def __init__(self, redis_service: RedisService, extract_service: ExtractService):
        self.redis_service = redis_service
        self.extract_service = extract_service
        self.lock = asyncio.Lock()
        self.executor = None
        
    async def get_all_books(self):
        asyncio.create_task(self.refresh_extract())
        books = await self.redis_service.get_all("books")
        return books
    
    async def get_by_id(self, book_id):
        asyncio.create_task(self.refresh_extract())
        book = await self.redis_service.get_value("books", f"book:{book_id}")
        return book
    
    async def filter_books(self, title: str, category: str):
        asyncio.create_task(self.refresh_extract())
        all_books = await self.get_all_books()
        result = [book for book in all_books if (title is None or title in book['title']) and (category is None or category in book['category'])]
        return result
    
    async def get_all_categories(self):
        asyncio.create_task(self.refresh_extract())
        all_categories = await self.redis_service.get_all("category_list")
        return all_categories
    
    
    async def refresh_extract(self):
        async with self.lock:
            last_update = await self.redis_service.get_last_update()
            if last_update and last_update.get("last_date"):
                last_date = datetime.fromisoformat(last_update["last_date"])
                now = datetime.now()
                if now - last_date < timedelta(hours=1):
                    return

            loop = asyncio.get_running_loop()
            if self.executor is None:
                from concurrent.futures import ThreadPoolExecutor
                self.executor = ThreadPoolExecutor(max_workers=2)

            data_to_redis, compiled_categories = await loop.run_in_executor(self.executor, self.extract_service.extract_books)
            
            await self.redis_service.save_all(ty='books', mapper=data_to_redis)
            await self.redis_service.save_all(ty='category_list', mapper=compiled_categories)
            await self.redis_service.update_last_date()
