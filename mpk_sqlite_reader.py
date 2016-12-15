from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from model.line_stop import LineStop
from model.mpk.line_stop import MpkLineStop
from model.mpk.stop import MpkStop
from model.stop import Stop
from settings import Config

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


def read_stops(sqlite_db):
    engine = create_engine('sqlite:///{0}'.format(sqlite_db))

    Base = declarative_base()
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    session_1 = DBSession()

    return session_1.query(MpkStop).all()


def read_line_stops(sqlite_db):
    engine = create_engine('sqlite:///{0}'.format(sqlite_db))

    Base = declarative_base()
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    session_2 = DBSession()

    return session_2.query(MpkLineStop).all()

if __name__ == '__main__':
    engine = create_engine(Config.DB_URI)

    Base = declarative_base()
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    stop_counter = 0
    line_stop_counter = 0

    session.query(Stop).delete(synchronize_session='evaluate')
    session.query(LineStop).delete(synchronize_session='evaluate')

    for s in read_stops('/home/marcin/mpk.sqlite'):
        stop = Stop(id=s.id, name=s.name, type=s.type, latitude=s.latitude, longitude=s.longitude)
        session.add(stop)

        stop_counter += 1

    for ls in read_line_stops('/home/marcin/mpk.sqlite'):
        for line in [s for s in ls.lines.split() if s]:
            line_stop = LineStop(line_id=ls.id, line_name=line)
            session.add(line_stop)

            line_stop_counter += 1

    session.commit()

    print('inserted {} stops'.format(stop_counter))
    print('inserted {} line stops'.format(line_stop_counter))
