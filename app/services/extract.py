from app.utils.functions import page_request, bs4_obj, html_parser, page_amount

base_url = "https://books.toscrape.com/"
page_url = "https://books.toscrape.com/catalogue/page-{}.html"

response = page_request(base_url)

soup = bs4_obj(response.text)

categorias = soup.find('div', class_='side_categories')

lista_categorias = []

for li in categorias.find('ul').find('li').find('ul').find_all('li'):
    categoria = li.get_text(strip=True)
    link = li.find('a')['href']
    dicionario = {
        'categoria': categoria,
        'link': link
    }

    lista_categorias.append(dicionario)

for link in lista_categorias['link'] and lista_categorias['categoria']:

    request = page_request(link)

    soup = bs4_obj(request.text)

    page_amt = page_amount(link)

    if page_amt==1:
        livros = html_parser(request.text)
    else:
        for page in range(1, page_amt+1):
            response = page_request(f'page-{page}.html')
            if response.status_code != 200:
                print(f"Erro na página: {page}")
                continue

            soup = bs4_obj(response.text)
            livros = html_parser(soup)        