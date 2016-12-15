from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from model.mpk.line_stop import MpkLineStop
from model.mpk.stop import MpkStop

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


def read_stops(sqlite_db):
    engine = create_engine('sqlite:///{0}'.format(sqlite_db))

    Base = declarative_base()
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    return session.query(MpkStop).all()


def read_line_stops(sqlite_db):
    engine = create_engine('sqlite:///{0}'.format(sqlite_db))

    Base = declarative_base()
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    return session.query(MpkLineStop).all()

if __name__ == '__main__':
    for s in read_stops('/home/marcin/mpk.sqlite'):
        print('{}'.format(s))

    for ls in read_line_stops('/home/marcin/mpk.sqlite'):
        print('{}'.format(ls))
