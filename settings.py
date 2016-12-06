import os
from os.path import join, dirname
from dotenv import load_dotenv

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


class Config:
    DB_NAME = os.environ.get('DB_NAME')
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = os.environ.get('DB_PORT')
    DB_URI = 'postgresql://{}:{}@{}:{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
