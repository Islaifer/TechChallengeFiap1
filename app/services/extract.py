from app.utils.functions import page_request, bs4_obj, html_parser, page_amount, json_text, save_json_file
from redis_service import RedisService
import datetime

# Criar uma classe com esse código com dependência de RedisService
# Salvar as categorias separadas com o método save do RedisService 
# pro endpoint de livros por categoria
# Salvar com campo de data da atualização 

class ExtractService:
    def __init__(self, redis_service: RedisService):
        self.redis_service = redis_service

    async def extract_and_save_books(self):
        redis_service = self.redis_service
        base_url = "https://books.toscrape.com/"
        response = page_request(base_url)
        soup = bs4_obj(response.text)
        categorias = soup.find('div', class_='side_categories')

        lista_categorias = []
        
        for li in categorias.find('ul').find('li').find('ul').find_all('li'):
            categoria = li.get_text(strip=True)
            url = li.find('a')['href']
            dicionario = {
                'categoria': categoria,
                'url': url
            }

            lista_categorias.append(dicionario)

        todos_livros = [
            {'last_updated': datetime.now()} 
        ]

        for item in lista_categorias:

            item_full_url = base_url + item['url']
            page_amt = page_amount(item_full_url)

            if page_amt==1:
                response = page_request(item_full_url)
                livros = html_parser(response.text)
                todos_livros.extend([
                    {**livro, 'categoria': item['categoria']} for livro in livros
                ])
            else:
                response = page_request(item_full_url)
                livros = html_parser(response.text)
                todos_livros.extend([
                    {**livro, 'categoria': item['categoria']} for livro in livros
                ])
                
                for page in range(2, page_amt+1):
                    page_url = item_full_url.replace('index.html', f'page-{page}.html')
                    response = page_request(page_url)
                    livros = html_parser(response.text)
                    todos_livros.extend([
                        {**livro, 'categoria': item['categoria']} for livro in livros
                    ])
            
            print(f"Categoria {item['categoria']} finalizada.")

        json_str = json_text(todos_livros)

        redis_service.save_all(ty='books', mapper=json_str)
        redis_service.rpush('category_list', lista_categorias)