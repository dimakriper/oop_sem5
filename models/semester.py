class Semester:
    def __init__(self, id, end_year, is_summer):
        self._id = id
        self._end_year = end_year
        self._is_summer = is_summer

    # Getter methods for Semester attributes
    @property
    def id(self):
        return self._id

    @property
    def end_year(self):
        return self._end_year

    @property
    def is_summer(self):
        return self._is_summer
