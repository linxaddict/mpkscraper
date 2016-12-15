from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'

Base = declarative_base()


class LineStop(Base):
    __tablename__ = 'line_stops'

    id = Column(String(128), primary_key=True)
    lines = Column(String, nullable=False)

    def __str__(self):
        return '{0}, {1}'.format(self.id, self.lines)
