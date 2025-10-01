from app.utils.functions import page_request, bs4_parser

if __name__=='__main__':
    base_url = "https://books.toscrape.com/"
    page_url = "https://books.toscrape.com/catalogue/page-{}.html"

    response = page_request(base_url)

    soup = bs4_parser(response.text)

    categorias = soup.find_all('div', class_='side_categories')

    for c in categorias:
        lista = []
        categoria = c.find('ul').find('li').find('ul').find('li').find('a').get_text(strip=True)
        lista.append(categoria)

    print(lista)