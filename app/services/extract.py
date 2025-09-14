import requests
from bs4 import BeautifulSoup

base_url = "https://books.toscrape.com/"
page_url = "https://books.toscrape.com/catalogue/page-{}.html"

def url_status(base_url) -> str:
    """
    função para verificar o status da base_url

    Args: base_url: str
    """
    page_request = requests.get(base_url)

    if page_request.status_code == 200:
        print("Conexão concluída com sucess. Cod:{page_request.status_code}")
    else: 
        print("Erro ao conectar com a api. Cod: {page_request.status_code} {page_request.reason}")

def html_parser(base_url: str, page_url: str) -> list:
    """
    função para extrair as informações dos livros e gravar em uma lista de dicts
    """
    

    for page in range(1,51):
        
        url = base_url if page==1 else page_url.format(page)

        page_request = requests.get(url=url)
        
        if page_request.status_code != 200:
            print("Erro na página: {page}")
            continue

        soup = BeautifulSoup(page_request.text, 'html.parser')
        
        # Encontrando os elementos HTML para parsear
        livros = soup.find_all('article', class_='product_pod')

        for livro in livros:
            titulo = livro.h3.a['title']
            preco = livro.find('p', class_='price_color').text
            disponibilidade = livro.find('p', class_='instock availability')
            imagem_url = livro.find('div', class_='image_container').a.img['src']
            # como pegar a qtd de estrelas?
            # onde encontrar a categoria?

            livro_dict = {
                'titulo': titulo,
                'preco': preco,
                'disponibilidade': disponibilidade,
                'imagem_url': imagem_url
                # rating
                # categoria
            }

            livros.append(livro_dict)