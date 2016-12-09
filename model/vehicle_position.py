import datetime

from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'

Base = declarative_base()


class VehiclePosition(Base):
    __tablename__ = 'vehicle_positions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False)
    type = Column(String(128), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    vehicle_id = Column(String(128), nullable=False)
    timestamp = Column(DateTime(timezone=True), onupdate=datetime.datetime.now)

    def __str__(self, *args, **kwargs):
        return '{0},{1},{2},{3},{4},{5},{6}'.format(self.id, self.name, self.type, self.latitude, self.longitude,
                                                    self.vehicle_id, self.timestamp)
