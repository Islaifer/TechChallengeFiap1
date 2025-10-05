import requests
from bs4 import BeautifulSoup

def page_request(base_url: str) -> str:
    """
    Função para fazer o request da página. Avalia o status_code, se for 200 retorna o request, senão encerra o programa.

    Args: base_url (str): URL base do site para fazer o request
    """
    page_request = requests.get(base_url)

    if page_request.status_code == 200:
        pass
    else: 
        HTTP_error = page_request.status_code
        print(f"Erro na requisição: {HTTP_error}")
    
    return page_request


def bs4_obj(html: str):
    """Recebe um HTML e retorna um objeto BeautifulSoup
    
    Args: html (str): HTML a ser parseado

    Returns: BeautifulSoup: Objeto BeautifulSoup
    """
    soup = BeautifulSoup(html, 'html.parser')
    
    return soup

def page_amount(base_url: str) -> int:
    """
    Função para retornar a quantidade de páginas do site.

    Args: base_url (str): URL base do site para fazer o request

    Returns: int: Quantidade de páginas do site
    """
    response = page_request(base_url)
    
    if response.status_code != 200:
        exit()
    
    soup = bs4_obj(response.text)
    
    page_slicer = soup.find('li', class_='current')

    if page_slicer:
        page_amount_int = int(page_slicer.get_text(strip=True).split()[-1])
    else:
        page_amount_int = 1
    
    return page_amount_int

def html_parser(html_response: str) -> dict:
    """
    Função para fazer o parser do HTML e retornar um dicionário com os dados extraídos dos livros.

    Args: HTML response (str): HTML response de um objeto BeautifulSoup

    Returns: dict: Dicionário com os dados extraídos dos livros (titulo, preço, disponibilidade,
    categoria, rating, url da imagem).
    """

    soup = bs4_obj(html_response)

    book_article = soup.find_all('article', class_='product_pod')

    livros = []

    for book in book_article:
        titulo = book.find('h3').find('a')['title']
        preco_text = book.find('div', class_='product_price').find('p', class_='price_color').text
        preco_float = float(preco_text.replace('£','').replace('Â','').strip())
        disponibilidade = book.find('div', class_='product_price').find('p', class_='instock availability').get_text(strip=True)
        imagem_url = book.find('div', class_='image_container').find('a').find('img', class_='thumbnail')['src']
        rating = book.find('p')['class'][1]

        livro_dict = {
            'titulo': titulo,
            'preco': preco_float,
            'disponibilidade': disponibilidade,
            'imagem_url': imagem_url,
            'rating': rating
        }
        
        livros.append(livro_dict)
    
    return livros