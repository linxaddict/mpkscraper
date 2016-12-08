import logging
import time
from datetime import datetime

import pytz
from geopy.distance import vincenty
from sqlalchemy.orm import Session

from model.api_vehicle_position import ApiVehiclePosition
from model.vehicle_position import VehiclePosition
from scraper.scraper import Scraper

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class ScrapingManager:
    MAX_LATITUDE_THRESHOLD = 90
    MAX_LONGITUDE_THRESHOLD = 180
    SCRAPE_TIMEOUT = 10
    LOG_FORMAT = '%(asctime)-15s %(message)s'
    LOG_FILE_NAME = 'errors.log'

    def _initialize_logger(self, logger):
        handler = logging.FileHandler(self.LOG_FILE_NAME)
        formatter = logging.Formatter(self.LOG_FORMAT)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.WARNING)

    @staticmethod
    def _write_to_file(position: ApiVehiclePosition, velocity: float, ts: datetime, ext='csv'):
        filename = '{0}.{1}'.format(position.name, ext)

        with open(filename, 'a') as file_out:
            line = '{0},{1},{2},{3},{4},{5}\n'.format(position.id, position.name, position.latitude,
                                                      position.longitude,
                                                      velocity, ts)
            file_out.write(line)

    def _valid_position(self, lat: float, lon: float) -> bool:
        return 0 <= lat < self.MAX_LATITUDE_THRESHOLD and 0 <= lon < self.MAX_LONGITUDE_THRESHOLD

    def __init__(self, scraper: Scraper, db_session: Session):
        super().__init__()

        self._last_positions = {}
        self._scraper = scraper
        self._db_session = db_session

        self._logger = logging.getLogger('mpk_scraper')
        self._initialize_logger(self._logger)

    def store_velocities(self, positions: [ApiVehiclePosition]) -> None:
        for p in positions:
            if not self._valid_position(p.latitude, p.longitude):
                continue

            if p.id in self._last_positions:
                lat, lon, dt = self._last_positions[p.id]
                now = datetime.now()

                if p.latitude != lat or p.longitude != lon:
                    self._last_positions[p.id] = (p.latitude, p.longitude, now)

                    distance = vincenty((lat, lon), (p.latitude, p.longitude)).meters
                    ts = (now - dt).total_seconds()

                    velocity_mps = distance / ts
                    velocity_kmph = velocity_mps * 3.6

                    print('[{0}:{1}] ({2}, {3}) {4:.2f} meters, {5:.2f} seconds, {6:.2f} km/h'.format(
                        p.name, p.id, p.latitude, p.longitude, distance, ts, velocity_kmph))

                    if velocity_kmph > 100:
                        print("last: ({0}, {1}), current: ({2}, {3})".format(lat, lon, p.latitude, p.longitude))

                    self._write_to_file(p, velocity_kmph, now)
            else:
                self._last_positions[p.id] = (p.latitude, p.longitude, datetime.now())
                self._write_to_file(p, 0, datetime.now())

    def start_scraping(self, timezone='Europe/Warsaw'):
        while True:
            # noinspection PyBroadException
            try:
                positions = self._scraper.fetch_positions()
                # store_velocities(positions)

                for p in positions:
                    vp = VehiclePosition()
                    vp.latitude = p.latitude
                    vp.longitude = p.longitude
                    vp.name = p.name
                    vp.type = p.type
                    vp.vehicle_id = p.id
                    vp.timestamp = datetime.now(pytz.timezone(timezone))

                    self._db_session.add(vp)
                    self._db_session.commit()

            except FileNotFoundError:
                self._logger.exception('error: specified config file does not exist')
            except ValueError:
                self._logger.exception('error: unable to parse json file')
            except Exception:
                self._logger.exception('unknown error')

            time.sleep(self.SCRAPE_TIMEOUT)
