import json

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class ScraperConfig:
    def __init__(self, bus_lines: [str], tram_lines: [str]):
        self._bus_lines = bus_lines
        self._tram_lines = tram_lines

    @property
    def bus_lines(self) -> [str]:
        return self._bus_lines

    @property
    def tram_lines(self) -> [str]:
        return self._tram_lines


class JsonConfigReader:
    KEY_BUS = 'bus'
    KEY_TRAM = 'tram'

    def read(self, config_file: str) -> ScraperConfig:
        with open(config_file) as file_in:
            config = json.load(file_in)

            bus_lines = config.get(self.KEY_BUS, [])
            tram_lines = config.get(self.KEY_TRAM, [])

        return ScraperConfig(bus_lines, tram_lines)


