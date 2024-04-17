from models.student import Student
from models.exams import ExamFactoryImpl
from models.major import Major
from models.semester import Semester
from models.department import Department
from dbservice import DatabaseAccessService

class Store:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self._db_service = DatabaseAccessService("academic-performance.db")
        self._exam_factory = ExamFactoryImpl()
        self._semesters = None
        self._departments = None
        self._majors = None
        self._students = None

    @property
    def semesters(self):
        if not self._semesters:
            self._load_semesters()
        return self._semesters

    @property
    def departments(self):
        if not self._departments:
            self._load_departments()
        return self._departments

    @property
    def majors(self):
        if not self._majors:
            self._load_majors()
        return self._majors

    @property
    def students(self):
        if not self._students:
            self._load_students()
        return self._students

    def _load_semesters(self):
        semesters_data = self._db_service.get_all_semesters()
        self._semesters = [Semester(data['id'], data['year_end'], data['is_summer']) for data in semesters_data]

    def _load_departments(self):
        departments_data = self._db_service.get_all_departments()
        self._departments = [Department(data['id'], data['name']) for data in departments_data]

    def _load_majors(self):
        majors_data = self._db_service.get_all_majors()
        self._majors = [Major(data['id'], data['name']) for data in majors_data]

    def _load_students(self):
        students = []
        students_data = self._db_service.get_all_students()
        for item in students_data:
            exams_data = self._db_service.get_student_exams(item['id'])
            exams = [self._exam_factory.create_exam(
                e['id'],
                e['student_id'],
                e['semester_id'],
                e['name'],
                e['status'],
                e['with-grade'],
                e['grade']
            ) for e in exams_data]
            student = Student(item['name'],
                              item['surname'],
                              item['patronym'],
                              item['major_id'],
                              item['department_id'],
                              exams
                              )
            students.append(student)
        self._students = students
