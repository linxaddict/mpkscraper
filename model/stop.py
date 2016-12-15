from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'

Base = declarative_base()


class Stop(Base):
    __tablename__ = 'stops'

    id = Column(String(128), primary_key=True)
    name = Column(String(128), nullable=False)
    type = Column(String(16), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    def __str__(self, *args, **kwargs):
        return '{0}, {1}, {2}, {3}, {4}'.format(self.id, self.name, self.type, self.latitude, self.longitude)
