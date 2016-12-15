from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'

Base = declarative_base()


class MpkStop(Base):
    __tablename__ = 'stops'

    id = Column(String(128), primary_key=True, name='symbol')
    name = Column(String(128), nullable=False, name='name')
    type = Column(String(16), nullable=False, name='type')
    latitude = Column(Float, nullable=False, name='y')
    longitude = Column(Float, nullable=False, name='x')

    def __str__(self, *args, **kwargs):
        return '{0}, {1}, {2}, {3}, {4}'.format(self.id, self.name, self.type, self.latitude, self.longitude)
