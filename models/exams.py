from abc import ABC, abstractmethod
class Exam:
    def __init__(self, id, student_id, semester_id, discipline_name, status):
        self._id = id
        self._student_id = student_id
        self._semester_id = semester_id
        self._discipline_name = discipline_name
        self._status = status

    # Getter methods for Exam attributes
    @property
    def id(self):
        return self._id

    @property
    def student_id(self):
        return self._student_id

    @property
    def semester_id(self):
        return self._semester_id

    @property
    def discipline_name(self):
        return self._discipline_name

    @property
    def status(self):
        return self._status

    @property
    def status_str(self):
        if self._status == 2:
            return "Зачет"
        elif self._status == 1:
            return "Незачёт"
        else:
            return " - "


class ExamWithGrade(Exam):
    def __init__(self, id, student_id, semester_id, discipline_name, status, grade):
        super().__init__(id, student_id, semester_id, discipline_name, status)
        self._grade = grade

    # Getter method for grade attribute
    @property
    def grade(self):
        return self._grade

    @property
    def status_str(self):
        grades = {2: "неудовл.", 3: "удовл.", 4: "хорошо", 5: "отлично"}
        if not self._status:
            return " - "
        else:
            return grades[self._grade]

class ExamFactory(ABC):
    @abstractmethod
    def create_exam(self, id, student_id, semester_id, discipline_name, status, with_grade, grade=None):
        pass

class ExamFactoryImpl(ExamFactory):
    def create_exam(self, id, student_id, semester_id, discipline_name, status, with_grade, grade=None):
        if with_grade != 1:
            return Exam(id, student_id, semester_id, discipline_name, status)
        else:
            return ExamWithGrade(id, student_id, semester_id, discipline_name, status, grade)