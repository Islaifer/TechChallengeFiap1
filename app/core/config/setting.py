import os

SERVICE_NAME = "Tech Challenge 1"
VERSION = "1.0.0"
DESCRIPTION = "Booker Scrapper for Tech Challenge 1"


DB_TYPE = os.getenv("DB_TYPE", "postgresql") # "postgresql" ou "mariadb"
DB_USER = os.getenv("DB_USER", "user")
DB_PASS = os.getenv("DB_PASS", "pass").replace("@", "%40")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "mydb")
DB_CONNECTOR = os.getenv("DB_CONNECTOR", "psycopg2") #pymysql ou psycopg2

DATABASE_URL = f"{DB_TYPE}+{DB_CONNECTOR}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


SECRET_KEY = os.getenv("JWT_SECRET_KEY", "12345678901234567890")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 4
