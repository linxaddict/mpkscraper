from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'

Base = declarative_base()


class LineStop(Base):
    __tablename__ = 'line_stops'

    id = Column(Integer, primary_key=True, autoincrement=True)
    line_id = Column(String(128), ForeignKey('stops.id'), primary_key=True)
    line_name = Column(String(128), nullable=False)

    def __str__(self):
        return '{0}, {1}, {2}'.format(self.id, self.line_id, self.lines)
