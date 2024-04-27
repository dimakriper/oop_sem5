import sqlite3


class DatabaseAccessService:
    def __init__(self, db_name):
        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d
        self.db_name = db_name
        self.connection = sqlite3.connect(db_name)
        self.connection.row_factory = dict_factory
        self.cursor = self.connection.cursor()



    def close(self):
        self.connection.close()

    def get_all_students(self):
        self.cursor.execute("SELECT * FROM Students")
        students = self.cursor.fetchall()
        return students

    def get_student_exams(self, student_id=0):

        query = f"""
            SELECT *
            FROM StudentExams 
            WHERE StudentExams.student_id = {student_id}
        """

        self.cursor.execute(query)

        return self.cursor.fetchall()
    def get_all_departments(self):
        self.cursor.execute("SELECT * FROM Departments")
        return self.cursor.fetchall()

    def get_all_majors(self):
        self.cursor.execute("SELECT * FROM Majors")
        return self.cursor.fetchall()

    def get_all_semesters(self):
        self.cursor.execute("SELECT * FROM Semesters")
        return self.cursor.fetchall()

    def insert_student(self, name, surname, patronym, department_id, major_id):
        try:
            self.cursor.execute("INSERT INTO Students (name, surname, patronym, department_id, major_id) VALUES (?, ?, ?, ?, ?)",
                                (name, surname, patronym, department_id, major_id))
            self.connection.commit()
            return 1
        except sqlite3.Error:
            return 0

    def insert_exam(self, student_id, semester_id, status, with_grade, grade, discipline_name):

        self.cursor.execute(
            "INSERT INTO StudentExams (student_id, semester_id, status, with_grade, grade, discipline_name) VALUES (?, ?, ?, ?, ?, ?)",
            (student_id, semester_id, status, with_grade, grade, discipline_name))
        self.connection.commit()



    def delete_student(self, student_id):
        try:
            self.cursor.execute(f"DELETE FROM Students WHERE id = {student_id}")
            self.connection.commit()
            return 1
        except sqlite3.Error:
            return 0
    def delete_exam(self, id):
        self.cursor.execute(f"DELETE FROM StudentExams WHERE id = {id}")
        self.connection.commit()