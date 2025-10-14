import requests
from bs4 import BeautifulSoup
import json

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

def json_text(data: dict) -> str:
    """
    Função para converter um dicionário em um objeto JSON.

    Args: data (dict): Dicionário a ser convertido em JSON

    Returns: JSON: Objeto JSON
    """
    json_data = json.dumps(data, indent=4, ensure_ascii=False)
    
    return json_data

def save_json_file(data: str, filename: str) -> None:
    """
    Função para salvar um dicionário em um arquivo JSON.

    Args: data (str): Dicionário a ser salvo em JSON, no formato string, pela função json_text
          filename (str): Nome do arquivo JSON
    """
    with open(filename, 'w', encoding='utf-8') as json_file:
        json_file.write(data)

def read_json_file(filename: str) -> dict:
    """
    Função para ler um arquivo JSON e retornar um dicionário.

    Args: filename (str): Nome do arquivo JSON

    Returns: dict: Dicionário com os dados do arquivo JSON
    """
    with open(filename, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    
    return data