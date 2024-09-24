import os
from dotenv import load_dotenv


load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = os.getenv('DEBUG', 'False') == 'True'

    # PostgreSQL config
    DB_NAME = os.getenv('NAME')
    DB_USER = os.getenv('USER')
    DB_PASSWORD = os.getenv('PASSWORD')
    DB_HOST = os.getenv('HOST')
    DB_PORT = os.getenv('PORT')

