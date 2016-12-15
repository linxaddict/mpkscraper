import datetime

from geopy.distance import vincenty
from sqlalchemy import Date
from sqlalchemy import and_
from sqlalchemy import cast
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from line_analyser import LineAnalyser
from model.vehicle_position import VehiclePosition
from model.vehicle_state import VehicleState
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
    results = [r for r in rows if r.timestamp.date() == datetime.date.today() and r.name == line_name]
    results.sort(key=lambda r: r.timestamp)

    return results


def compute_velocities(positions: [VehiclePosition]) -> [VehicleState]:
    last_positions = {}
    results = []

    for p in positions:
        if p.vehicle_id in last_positions:
            lat, lon, dt = last_positions[p.vehicle_id]
            last_positions[p.vehicle_id] = (p.latitude, p.longitude, p.timestamp)

            distance = vincenty((lat, lon), (p.latitude, p.longitude)).meters
            ts = (p.timestamp - dt).total_seconds()

            velocity_mps = distance / ts
            velocity_kmph = velocity_mps * 3.6

            results.append(VehicleState(p, velocity_kmph))
        else:
            last_positions[p.vehicle_id] = (p.latitude, p.longitude, p.timestamp)
            results.append(VehicleState(p, 0.0))

    return results


def remove_redundant_states(states: [VehicleState]) -> [VehicleState]:
    results = []
    last_was_zero = False

    for s in states:
        if s.velocity > 100:
            continue

        if s.velocity == 0 and not last_was_zero:
            results.append(s)
            last_was_zero = True
        elif s.velocity != 0:
            results.append(s)
            last_was_zero = False

    return results


if __name__ == '__main__':
    engine = create_engine(Config.DB_URI)

    Base = declarative_base()
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    today = session.query(VehiclePosition).filter(
        and_(VehiclePosition.name == '8', cast(VehiclePosition.timestamp, Date) == datetime.date.today())).all()
    # today = filter_today_with_line_name(rows, '8')

    analyser = LineAnalyser()
    courses = analyser.extract_courses('8', today)

    for c in courses:
        print('{}'.format(c))

        # states = compute_velocities(today)
        #
        # zero_velocity = [vs for vs in states if vs.velocity == 0]
        # filtered = remove_redundant_states(states)
        #
        # print('states: {0}'.format(len(states)))
        # print('zero velocity: {0}'.format(len(zero_velocity)))
        # print('filtered: {0}'.format(len(filtered)))

        # velocities = [v.velocity for v in filtered]
        # dates = [v.timestamp for v in filtered]
        #
        # plt.plot(dates[12000:12100], velocities[10000:10100])
        # plt.ylabel('velocity')
        # plt.show()

        # for row in rows:
        #     print('{0}'.format(row))
        #
        # save_as_csv(rows)

        # with open('velocities.csv', 'w') as file_out:
        #     file_out.write('id,name,type,latitude,longitude,vehicle_id,timestamp\n')
        #
        #     for r in rows:
        #         file_out.write(str(r))
        #         file_out.write('\n')
        #
        # csv_rows = []
        # for state in filtered[5:]:
        #     row = [filtered]
