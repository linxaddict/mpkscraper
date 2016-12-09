import datetime

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from model.vehicle_position import VehiclePosition
from settings import Config

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


def save_as_csv(rows, filename='vehicle_positions.csv'):
    with open(filename, 'w') as file_out:
        file_out.write('id,name,type,latitude,longitude,vehicle_id,timestamp\n')

        for r in rows:
            file_out.write(str(r))
            file_out.write('\n')


def filter_today_with_line_name(rows, line_name):
    return [r for r in rows if r.timestamp.date() == datetime.date.today() and r.name == line_name]


if __name__ == '__main__':
    engine = create_engine(Config.DB_URI)

    Base = declarative_base()
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    rows = session.query(VehiclePosition)

    for row in rows:
        print('{0}'.format(row))

    save_as_csv(rows)
