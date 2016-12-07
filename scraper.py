import json

import requests

from config_reader import ScraperConfig

from model.api_vehicle_position import ApiVehiclePosition

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class Scraper:
    URL = 'http://mpk.wroc.pl/position.php'
    KEY_BUS_LINE = 'busList[bus][]'
    KEY_TRAM_LINE = 'busList[tram][]'

    def _prepare_form_data(self) -> {str, str}:
        data = {}

        if self.config.bus_lines:
            data[self.KEY_BUS_LINE] = self.config.bus_lines

        if self.config.tram_lines:
            data[self.KEY_TRAM_LINE] = self.config.tram_lines

        return data

    def __init__(self, config: ScraperConfig):
        self._config = config

    def fetch_positions(self) -> [ApiVehiclePosition]:
        form_data = self._prepare_form_data()
        r = requests.post(self.URL, form_data)
        print('fetched: {0}'.format(r.text))

        return [ApiVehiclePosition(**p) for p in json.loads(r.text)]

    @property
    def config(self) -> ScraperConfig:
        return self._config
