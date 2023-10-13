import os
from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())
basedir = os.path.abspath(os.path.dirname(__file__))


user = os.getenv('POSTGRES_USER')
psw = os.getenv('POSTGRES_PASSWORD')
database = os.getenv('POSTGRES_DB')
secret_key = os.getenv('SECRET_KEY')
dbhost = os.getenv('DB_HOST')


class Config:
    SQLALCHEMY_DATABASE_URI = f'postgresql://{user}:{psw}@db/{database}'
    SECRET_KEY = secret_key
