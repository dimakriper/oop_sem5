class Student:
    def __init__(self, name, surname, patronym, major_id, department_id, exams):
        self._name = name
        self._surname = surname
        self._patronym = patronym
        self._major_id = major_id
        self._department_id = department_id
        self._exams = exams

    @property
    def full_name(self):
        return f'{self._name} {self._patronym} {self._surname}'

    @property
    def name(self):
        return self._name

    @property
    def surname(self):
        return self._surname

    @property
    def patronym(self):
        return self._patronym

    @property
    def department_id(self):
        return self._department_id

    @property
    def major_id(self):
        return self._major_id

    @property
    def exams(self, semester_id=None):
        if semester_id:
            return filter(lambda exam: exam.semester_id == semester_id, self._exams)
        else:
            return self._exams
