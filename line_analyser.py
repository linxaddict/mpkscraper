from typing import List

from model.vehicle_position import VehiclePosition

__author__ = 'Marcin Przepiórkowski'
__email__ = 'mprzepiorkowski@gmail.com'


class LineAnalyser:
    class Course:
        def __init__(self, name, course_id, positions, length):
            super().__init__()

            self._name = name
            self._course_id = course_id
            self._positions = positions
            self._length = length

        @property
        def name(self):
            return self._name

        @property
        def course_id(self):
            return self._course_id

        @property
        def positions(self):
            return self._positions

        @property
        def length(self):
            return self._length

        @property
        def start(self):
            return self._positions[0] if self._positions else None

        @property
        def end(self):
            return self._positions[len(self._positions) - 1] if self._positions else None

        def __str__(self, *args, **kwargs):
            return '[{0}] id: {1}, positions: {2}, start: ({3}, {4}), end: ({5}, {6}), length: {7:.2f} min'.format(
                self.name, self.course_id, len(self.positions), self.start.latitude, self.start.longitude,
                self.end.latitude, self.end.longitude, self.length.total_seconds() / 60)

    def extract_courses(self, line_name: str, positions: List[VehiclePosition]) -> List[Course]:
        courses = {}
        courses_list = []

        for p in positions:
            if p.vehicle_id not in courses:
                courses[p.vehicle_id] = []

            courses[p.vehicle_id].append(p)

        for key, _ in courses.items():
            courses[key].sort(key=lambda r: r.timestamp)

        for key, positions in courses.items():
            if len(positions) > 1:
                first_p = positions[0]
                last_p = positions[len(positions) - 1]

                time = last_p.timestamp - first_p.timestamp

                courses_list.append(self.Course(line_name, key, positions, time))

        return courses_list
