from app.utils.functions import page_request, bs4_parser

if __name__=='__main__':
    base_url = "https://books.toscrape.com/"
    page_url = "https://books.toscrape.com/catalogue/page-{}.html"

    response = page_request(base_url)

    soup = bs4_parser(response.text)

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


print(lista_categorias)