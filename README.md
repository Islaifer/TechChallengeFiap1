
# Tech Challenge 1

## Autores
- Adryen Simões de Oliveira
- Matheus Roberto Alves Andrade

## Descrição

Este projeto representa o Tech Challenge 1 da FIAP para o curso de Machine Learning Engineering.

O objetivo do projeto é fazer um web scrapping do site https://books.toscrape.com/, que é um site que disponibiliza dados para prática de web scrapping. Após o scrapping, disponibilizar endpoints para disponibilizar os dados coletados.

## Como usar
A API estará disponível no host https://techchallengefiap1-production.up.railway.app
Para usar, basta criar uma conta com o endpoint de registro, fazer login com os dados registrados, e por fim, utilizar os endpoints de serviço passando o token jwt no header como Authorization Bearer.

### Documentação da API

O projeto disponibiliza das seguintes rotas de api (Essas informações podem ser encontradas na rota /doc, onde é montado um swagger para as mesmas):

#### /api/v1/health
Verbo http: GET

Response Body (retorna 200):
```json
{
  "status": "string",
  "timestamp": "string"
}
```
Descrição: Essa rota serve para verificar o status da API, se ela está disponível ou não.

#### /auth/register
Verbo http: POST

Request Body:
```json
{
  "name": "string",
  "email": "string",
  "password": "string"
}
```

Response Body (retorna 200):
```json
{
  "id": 0
  "name": "string",
  "email": "string",
  "password": "********"
}
```
Descrição: Essa rota serve para registrar novos usuários, onde o email e name devem ser únicos e o email deve ser válido.

#### /auth/login
Verbo http: POST

Request Body:
```json
{
  "name": "string",
  "email": "string",
  "password": "string"
}
```

Response Body:
```json
"token"
```
Descrição: Essa rota serve para autenticação via JWT. Ela recebe um json contendo as informações de login, e retorna um token jwt, que é usado para autenticar nas rotas protegidas.

#### /api/v1/books
Verbo http: GET

Requer passar Token jwt no Authorization como bearer:
```bash
Authorization: Bearer TOKEN
```

Response Body:
```json
[
  {
    "id": "string",
    "title": "string",
    "category": "string",
    "price": 0,
    "availability": "string",
    "image_url": "string",
    "rating": "string",
    "last_updated": "string"
  }
]
```
Descrição: Essa rota é uma rota protegida que serve para buscar todos os livros obtidos no scrapping.

#### /api/v1/books/{book_id}
Verbo http: GET

Path Parameter:
- {book_id}: Id do book

Requer passar Token jwt no Authorization como bearer:
```bash
Authorization: Bearer TOKEN
```

Response Body:
```json
{
  "id": "string",
  "title": "string",
  "category": "string",
  "price": 0,
  "availability": "string",
  "image_url": "string",
  "rating": "string",
  "last_updated": "string"
}
```
Descrição: Essa rota é uma rota protegida que serve para buscar um livro específico na base de dados obtidido pelo scrapping através do id dele.

#### /api/v1/books/search
Verbo http: GET

Query Parameters:
- title: Título do livro
- category: Categoria do livro

Requer passar Token jwt no Authorization como bearer:
```bash
Authorization: Bearer TOKEN
```

Response Body:
```json
[
  {
    "id": "string",
    "title": "string",
    "category": "string",
    "price": 0,
    "availability": "string",
    "image_url": "string",
    "rating": "string",
    "last_updated": "string"
  }
]
```
Descrição: Essa rota é uma rota protegida que serve para buscar os livros obtidios pelo scrapping, filtrando pelo nome e pela categoria.

#### /api/v1/categories
Verbo http: GET

Requer passar Token jwt no Authorization como bearer:
```bash
Authorization: Bearer TOKEN
```

Response Body:
```json
[
  {
    "category": "string",
    "url": "string"
  }
]
```
Descrição: Essa rota é uma rota protegida que serve para buscar todas as categorias obtidas pelo scrapping.

#### /api/v1/stats/overview
Verbo http: GET

Requer passar Token jwt no Authorization como bearer:
```bash
Authorization: Bearer TOKEN
```

Response Body:
```json
[
  {
    "total_books": 0,
    "average_price": 0,
    "top_books": [
      {
        "id": "string",
        "title": "string",
        "price": 53.82,
        "availability": "string",
        "image_url": ".string",
        "rating": "string",
        "category": "string",
        "last_updated": "string"
      }
    ]
]
```
Descrição: Essa rota é uma rota protegida que serve para fazer um overview geral sobre os dados obtidos pelo scrapping.

#### /api/v1/stats/top-rated/{n}
Verbo http: GET

Path Parameter:
- {n}: Número de itens que vão ser considerados no top (top 5, top 10... top n)

Requer passar Token jwt no Authorization como bearer:
```bash
Authorization: Bearer TOKEN
```

Response Body:
```json
[
  {
    "top_books": [
      {
        "id": "string",
        "title": "string",
        "price": 53.82,
        "availability": "string",
        "image_url": ".string",
        "rating": "string",
        "category": "string",
        "last_updated": "string"
      }
    ]
  }
]
```
Descrição: Essa rota é uma rota protegida que serve para buscar os livros com maiores ratings obtidos pelo scrapping.

#### /api/v1/stats/categories
Verbo http: GET

Requer passar Token jwt no Authorization como bearer:
```bash
Authorization: Bearer TOKEN
```

Response Body:
```json
{
  "avg_price_by_category": {},
  "book_by_category": {}
}
```
Descrição: Essa rota é uma rota protegida que serve para buscar o preço médio por categoria e o número de livros por categoria obtidos no scrapping.

## Funcionamento

Uma imagem geral do fluxo de funcionamento se encontra dentro de /docs aqui no repositório.

Esse projeto é feito em FastApi, e toda vez que ele sobe, é feito um scrapping no site https://books.toscrape.com/, buscando todos os dados e os guardando no Redis. Junto com isso, é registrado a data atual, para saber qual foi a última vez que o dado foi atualizado.

Após isso, a API sobe normalmente, pegando os dados diretamente do Redis, porém, toda chamada é feita uma validação para ver a última atualização dos dados, caso a última atualização foi feita a mais de 1 hora, a api retorna os dados normalmente para o cliente, mas cria uma task em background que realiza novamente o scrapping dos dados, assim os dados sempre ficam atualizados, garantindo assim a integridade dos mesmos e a velocidade na entrega dos dados para o usuário.

### Arquitetura
A arquitetura do projeto foi escolhida a arquitetura em camadas, ou seja, nossa arquitetura é limpa e escalável, sendo fácil a evolução sem a necessidade de mexer em todo o projeto para cada alteração necessária.

### Escolhas do projeto
Foi escolhido o framework do FastApi pela sua velocidade e praticidade em disponibilizar endpoints.

O banco de dados relacional MariaDB foi escolhido para salvar os dados de login dos usuários, podendo evoluir para guardar dados de métricas de uso por usuário futuramente.

O banco de dados não relacional Redis foi escolhido por conta da sua velocidade de leitura e escrita, fazendo assim com que o processamento seja muito mais rápido para o usuário, ainda mais pensando no volume de dados que pode crescer, ou seja, mesmo que o volume acabe se tornando maior, a resposta ainda continuará sendo rápida por conta da rápida resposta do Redis (que escreve os dados na memória).

### Cenários de Uso e Integrações futuras
Um cientista de dados/ML pode utilizar das chamadas de maneira rápida para análise de dados, e estar garantido da integridade e atualização dos dados disponibilizados.

Além disso, por conta da velocidade de entrega dos dados, é perfeito para integração com modelos de Machine Learning, podendo utilizar das chamadas para alimentar dados de treinamento e teste para essas ML's.

## Instalação e Uso
Caso queira instalar e utilizar o projeto localmente, nessa sessão vamos ensinar a instalar e rodar o projeto.

O projeto foi feito para rodar em docker, porém é possível rodá-lo fora do docker.

### Requisitos
Os requisitos para a instalação e utilização desse projeto são:
- docker e docker compose

Se for rodar fora de docker, serão necessários os requisitos:
- redis
- mariadb

### Como instalar

Vá até o diretório que se encontra o projeto em sua máquina.

(Opcional)
Na pasta raíz do projeto possui o arquivo de docker-compose (docker-compose.yml), nele será possível fazer as modificações de acordo com suas necessidades.

#### Para Windows

Utilize o power shell e execute:

```bash
  Start-Process "docker-compose" "-f docker-compose.yml up --build" -Verb RunAs
``` 

Nota para usuários de windows:
Caso seu sistema de política de execução do power shell seja Restricted, então será necessário mudar temporariamente para executar o script. Para fazer a alteração temporária, utilize:

```bash
  Set-ExecutionPolicy RemoteSigned -Scope Process
```

#### Para Linux

Dê permissão de execução ao script e o execute:

```bash
  sudo docker-compose up --build
```

### Rodando sem docker
Para rodar sem docker, primeiro configure as variáveis de ambiente:
- REDIS_HOST: host_do_redis
- REDIS_PORT: porta_do_redis
- REDIS_PASS: senha_do_redis #opcional
- REDIS_USER: usuario_do_redis #opcional
- DB_TYPE: tipo_do_banco #postgresql ou mariadb
- DB_USER: usuario_do_banco
- DB_PASS: senha_do_banco
- DB_HOST: host_do_banco
- DB_PORT: porta_do_banco
- DB_NAME: nome_do_banco
- DB_CONNECTOR: connector #pymysql ou psycopg2

Instale as dependencias do projeto com:

```bash
  poetry install
```

E por fim, basta executar o projeto com:

```bash
  poetry run uvicorn app.main:app
```

## Uso
Após isso, o projeto estará rodando em sua máquina na porta 8000.

Com o projeto rodando via docker, basta acessar as chamadas de api pelo host localhost:8000.