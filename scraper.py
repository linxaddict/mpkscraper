import requests

from config_reader import ScraperConfig
from typing import Dict

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class Scraper:
    URL = 'http://mpk.wroc.pl/position.php'
    KEY_BUS_LINE = 'busList[bus][]'
    KEY_TRAM_LINE = 'busList[tram][]'

    def _prepare_form_data(self) -> Dict[str, str]:
        bus = {self.KEY_BUS_LINE: line for line in self.config.bus_lines}
        tram = {self.KEY_TRAM_LINE: line for line in self.config.tram_lines}

        return {**bus, **tram}

    def __init__(self, config: ScraperConfig):
        self._config = config

    def scrape(self):
        form_data = self._prepare_form_data()
        r = requests.post(self.URL, form_data)

        print(r.text)

    @property
    def config(self) -> ScraperConfig:
        return self._config
