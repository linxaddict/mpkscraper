from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config_reader import JsonConfigReader
from scraper.scraper import Scraper
from scraper.scraping_manager import ScrapingManager
from settings import Config

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


def start_scraping():
    config_reader = JsonConfigReader()
    engine = create_engine(Config.DB_URI)

    Base = declarative_base()
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    config = config_reader.read('config.json')
    scraper = Scraper(config)

    scraping_manager = ScrapingManager(scraper, session)
    scraping_manager.start_scraping()

if __name__ == '__main__':
    start_scraping()
