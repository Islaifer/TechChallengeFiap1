from app.utils.functions import page_request, bs4_obj, html_parser, page_amount, json_text, save_json_file
from typing import Any, Dict, Tuple
from app.services.redis_service import RedisService
from datetime import datetime
import asyncio

# Criar uma classe com esse código com dependência de RedisService
# Salvar as categorias separadas com o método save do RedisService 
# pro endpoint de livros por category
# Salvar com campo de data da atualização 

class ExtractService:
    def __init__(self, redis_service: RedisService):
        self.redis_service = redis_service
        
    def extract_and_save_books(self):
        redis_service = self.redis_service
        
        data_to_redis, compiled_categories = self.extract_books();

        asyncio.create_task(redis_service.save_all(ty='books', mapper=data_to_redis)) 
        asyncio.create_task(redis_service.save_all(ty='category_list', mapper=compiled_categories)) 
        asyncio.create_task(redis_service.update_last_date())
        
    def extract_books(self) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        base_url = "https://books.toscrape.com/"
        response = page_request(base_url)
        soup = bs4_obj(response.text)
        categorias = soup.find('div', class_='side_categories')

        lista_categorias = []
        
        for li in categorias.find('ul').find('li').find('ul').find_all('li'):
            category = li.get_text(strip=True)
            url = li.find('a')['href']
            dicionario = {
                'category': category,
                'url': url
            }

            lista_categorias.append(dicionario)
            
        compiled_categories: Dict[str, Any] = { f"CATEGORY:{category['category']}": category for category in lista_categorias }

        todos_livros = []
        
        date_now = datetime.now().isoformat()

        for item in lista_categorias:

            item_full_url = base_url + item['url']
            page_amt = page_amount(item_full_url)

            response = page_request(item_full_url)
            livros = html_parser(response.text)
            todos_livros.extend([
                {**livro, 'category': item['category'], 'last_updated': date_now} for livro in livros
            ])
            if page_amt > 1:
                for page in range(2, page_amt+1):
                    page_url = item_full_url.replace('index.html', f'page-{page}.html')
                    response = page_request(page_url)
                    livros = html_parser(response.text)
                    todos_livros.extend([
                        {**livro, 'category': item['category'], 'last_updated': date_now} for livro in livros
                    ])
            
            print(f"Categoria {item['category']} finalizada.")

        #json_str = json_text(todos_livros)
        
        data_to_redis: Dict[str, Any] = {f"book:{livro['id']}": livro for livro in todos_livros}
        
        return data_to_redis, compiled_categories