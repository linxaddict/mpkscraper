import time
import pytz

from json import JSONDecodeError

from sqlalchemy.ext.declarative import declarative_base

from config_reader import JsonConfigReader
from model.api_vehicle_position import ApiVehiclePosition
from model.vehicle_position import VehiclePosition
from scraper import Scraper
from geopy.distance import vincenty
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import Config

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'

MAX_LATITUDE_THRESHOLD = 90
MAX_LONGITUDE_THRESHOLD = 180


def valid_position(lat: float, lon: float) -> bool:
    return 0 <= lat < MAX_LATITUDE_THRESHOLD and 0 <= lon < MAX_LONGITUDE_THRESHOLD


def write_to_file(position: ApiVehiclePosition, velocity: float, ts: datetime, ext='csv'):
    filename = '{0}.{1}'.format(position.name, ext)

    with open(filename, 'a') as file_out:
        line = '{0},{1},{2},{3},{4},{5}\n'.format(position.id, position.name, position.latitude, position.longitude,
                                                  velocity, ts)
        file_out.write(line)


if __name__ == '__main__':
    config_reader = JsonConfigReader()
    last_positions = {}

    engine = create_engine(Config.DB_URI)
    Base = declarative_base()
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    vp = VehiclePosition()
    vp.latitude = 12.1
    vp.longitude = 14.2
    vp.name = 'test_name'
    vp.type = 'test_type'
    vp.vehicle_id = 'test_id'
    vp.timestamp = datetime.now(pytz.timezone('Europe/Warsaw'))

    session.add(vp)
    session.commit()

    try:
        config = config_reader.read('config.json')

        print('bus lines: {0}'.format(config.bus_lines))
        print('tram lines: {0}'.format(config.tram_lines))

        scraper = Scraper(config)

        while True:
            positions = scraper.fetch_positions()

            for p in positions:
                if not valid_position(p.latitude, p.longitude):
                    continue

                if p.id in last_positions:
                    lat, lon, dt = last_positions[p.id]
                    now = datetime.now()

                    if p.latitude != lat or p.longitude != lon:
                        last_positions[p.id] = (p.latitude, p.longitude, now)

                        distance = vincenty((lat, lon), (p.latitude, p.longitude)).meters
                        ts = (now - dt).total_seconds()

                        velocity_mps = distance / ts
                        velocity_kmph = velocity_mps * 3.6

                        print('[{0}:{1}] ({2}, {3}) {4:.2f} meters, {5:.2f} seconds, {6:.2f} km/h'.format(
                            p.name, p.id, p.latitude, p.longitude, distance, ts, velocity_kmph))

                        if velocity_kmph > 100:
                            print("last: ({0}, {1}), current: ({2}, {3})".format(lat, lon, p.latitude, p.longitude))

                        write_to_file(p, velocity_kmph, now)
                else:
                    last_positions[p.id] = (p.latitude, p.longitude, datetime.now())
                    write_to_file(p, 0, datetime.now())

            time.sleep(5)
    except FileNotFoundError:
        print('error: specified config file does not exist')
    except JSONDecodeError as err:
        print('error: unable to parse json file: {0}'.format(err))
