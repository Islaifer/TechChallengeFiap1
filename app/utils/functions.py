import requests
from bs4 import BeautifulSoup

def page_request(base_url: str) -> str:
    """
    função para verificar o status da base_url

    Args: base_url: str
    """
    page_request = requests.get(base_url)

    if page_request.status_code == 200:
        pass
    else: 
        exit()
    
    return page_request


def bs4_parser(html: str):
    """Recebe um HTML e retorna um objeto BeautifulSoupa"""
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def html_parser(base_url: str, page_url: str) -> list:
    """
    função para extrair as informações dos livros e gravar em uma lista de dicts
    """

    resultado = []
    
    for page in range(1,51):
        
        url = base_url if page==1 else page_url.format(page)

        response = page_request(url)
        
        if response.status_code != 200:
            print(f"Erro na página: {page}")
            continue

        soup = bs4_parser(response.text)
        
        # Encontrando os elementos HTML para parsear
        livros = soup.find_all('article', class_='product_pod')

        for livro in livros:
            titulo = livro.find('h3').find('a')['title']
            preco = livro.find('div', class_='product_price').find('p', class_='price_color').text
            disponibilidade = livro.find('div', class_='product_price').find('p', class_='instock availability').get_text(strip=True)
            imagem_url = livro.find('div', class_='image_container').find('a').find('img', class_='thumbnail')['src']
            rating = livro.find('p')['class']
            # onde encontrar a categoria?

            livro_dict = {
                'titulo': titulo,
                'preco': preco,
                'disponibilidade': disponibilidade,
                'imagem_url': imagem_url,
                'rating': rating[1]
                # categoria
            }

            resultado.append(livro_dict)
    
    return resultado

if __name__=='__main__':
    base_url = "https://books.toscrape.com/"
    page_url = "https://books.toscrape.com/catalogue/page-{}.html"

    r = page_request(base_url)
    p = bs4_parser(r.text)
    resultado = html_parser(base_url,page_url)
    print(resultado)