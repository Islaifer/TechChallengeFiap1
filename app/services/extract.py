from app.utils.functions import page_request, bs4_obj, html_parser, page_amount

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

todos_livros = []

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