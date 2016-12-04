from json import JSONDecodeError

from config_reader import JsonConfigReader
from scraper import Scraper

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


if __name__ == '__main__':
    config_reader = JsonConfigReader()

    try:
        config = config_reader.read('config.json')

        print('bus lines: {0}'.format(config.bus_lines))
        print('tram lines: {0}'.format(config.tram_lines))

        scraper = Scraper(config)
        scraper.scrape()
    except FileNotFoundError:
        print('error: specified config file does not exist')
    except JSONDecodeError:
        print('error: unable to parse json file')
