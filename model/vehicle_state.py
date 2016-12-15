from model.vehicle_position import VehiclePosition


class VehicleState:
    def __init__(self, vehicle_position: VehiclePosition, velocity: float):
        super().__init__()

        self._vehicle_position = vehicle_position
        self._velocity = velocity

    @property
    def name(self):
        return self._vehicle_position.name

    @property
    def type(self):
        return self._vehicle_position.type

    @property
    def longitude(self):
        return self._vehicle_position.longitude

    @property
    def latitude(self):
        return self._vehicle_position.latitude

    @property
    def vehicle_id(self):
        return self._vehicle_position.vehicle_id

    @property
    def timestamp(self):
        return self._vehicle_position.timestamp

    @property
    def velocity(self):
        return self._velocity

    def __str__(self, *args, **kwargs):
        return '{0},{1},{2},{3},{4},{5},{6}'.format(self.name, self.type, self.latitude, self.longitude,
                                                    self.vehicle_id, self.timestamp, self.velocity)
