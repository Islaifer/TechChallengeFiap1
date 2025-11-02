# Usa Python 3.12 slim como base
FROM python:3.12-slim

# Evita que o Python gere arquivos .pyc e define o UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    python3-dev \
    curl \
 && rm -rf /var/lib/apt/lists/*
 
# Instala Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Adiciona Poetry ao PATH
ENV PATH="/root/.local/bin:$PATH"

# Cria diretório da aplicação
WORKDIR /app

# Copia os arquivos do projeto
COPY pyproject.toml poetry.lock ./

# Instala dependências via Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copia todo o código da aplicação
COPY . .

# Expõe porta da API
EXPOSE 8000

# Comando para rodar o FastAPI com Uvicorn
CMD ["./wait-for-it.sh", "mariadb", "3306", "--", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]