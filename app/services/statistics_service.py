from app.core.config.redis_settings import RedisConnection
from redis_service import RedisService
import matplotlib.pyplot as plt

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
    
    def average_price(self):
        """Retorna o preço médio dos livros na fonte de dados."""

        books = self.redis.service.get_all("books")

        if books is not None:
            total_price = sum(book['price'] for book in books)
            average_price = total_price / len(books)
            return print(f'O preço médio dos livros é: {average_price:.2f}')
        else:
            return None
        
    def rating_histogram(self):
        """Retorna um histograma de avaliações dos livros na fonte de dados."""

        books = self.redis.service.get_all("books")

        if books is not None:
            ratings = [book['rating'] for book in books]
            plt.hist(ratings, bins=10, edgecolor='black')
            plt.title('Histograma de Avaliações dos Livros')
            plt.xlabel('Avaliação')
            plt.ylabel('Número de Livros')
            plt.show()
    
    def top_rated_books(self, n=5):
        """Retorna os n livros mais bem avaliados na fonte de dados."""

        books = self.redis.service.get_all("books")

        if books is not None:
            sorted_books = sorted(books, key=lambda x: x['rating'], reverse=True)
            top_books = sorted_books[:n]
            return top_books
        else:
            return None
        
    def avg_price_by_category(self):
        """Retorna o preço médio dos livros por categoria na fonte de dados."""

        books = self.redis.service.get_all("books")

        if books is not None:
            category_price = {}
            category_count = {}

            for book in books:
                category = book['category']
                price = book['price']

                if category in category_price:
                    category_price[category] += price
                    category_count[category] += 1
                else:
                    category_price[category] = price
                    category_count[category] = 1

            avg_price_category = {category: category_price[category] / category_count[category] for category in category_price}
            return avg_price_category
        else:
            return None
        
    def book_amount_by_category(self):
        """Retorna a quantidade de livros por categoria na fonte de dados."""

        books = self.redis.service.get_all("books")

        if books is not None:
            category_count = {}

            for book in books:
                category = book['category']

                if category in category_count:
                    category_count[category] += 1
                else:
                    category_count[category] = 1
            
        return category_count