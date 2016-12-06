__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class ApiVehiclePosition:
    KEY_NAME = 'name'
    KEY_TYPE = 'type'
    KEY_LATITUDE = 'x'
    KEY_LONGITUDE = 'y'
    KEY_VEHICLE_ID = 'k'

    def __init__(self, **kwargs):
        super().__init__()

        self._name = kwargs.get(self.KEY_NAME)
        self._type = kwargs.get(self.KEY_TYPE)
        self._latitude = kwargs.get(self.KEY_LATITUDE)
        self._longitude = kwargs.get(self.KEY_LONGITUDE)
        self._id = kwargs.get(self.KEY_VEHICLE_ID)

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> str:
        return self._type

    @property
    def latitude(self) -> float:
        return self._latitude

    @property
    def longitude(self) -> float:
        return self._longitude

    @property
    def id(self) -> int:
        return self._id

    def __str__(self, *args, **kwargs):
        return "[{0}:{1}] ({2}): {3}, {4}".format(self.name, self.id, self.type, self.latitude, self.longitude)
