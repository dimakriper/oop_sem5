class Semester:
    def __init__(self, id, end_year, is_summer):
        self._id = id
        self._end_year = end_year
        self._is_summer = is_summer


    @property
    def name(self):

        return f'{self._end_year-1}/{self._end_year} {"весенний" if self._is_summer == 1 else "осенний"}'
    @property
    def id(self):
        return self._id

    @property
    def end_year(self):
        return self._end_year

    @property
    def is_summer(self):
        return self._is_summer
