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

    def update_student(self, student_id,  name, surname, patronym, department_id, major_id):
        try:
            self.cursor.execute("UPDATE Students SET name=?, surname=?, patronym=?, department_id=?, major_id=? WHERE id=?",
                                (name, surname, patronym, department_id, major_id, student_id))
            self.connection.commit()
            return 1
        except sqlite3.Error:
            raise sqlite3.Error
            return 0

    def insert_exam(self, student_id, semester_id, status, with_grade, grade, discipline_name):
        try:
            # Check if the exam already exists for the given student, semester, and discipline
            self.cursor.execute(
                "SELECT COUNT(*) FROM StudentExams WHERE student_id = ? AND semester_id = ? AND discipline_name = ?",
                (student_id, semester_id, discipline_name))
            exists = self.cursor.fetchone()['COUNT(*)']

            if exists:
                # Update the existing exam
                self.cursor.execute(
                    "UPDATE StudentExams SET status=?, with_grade=?, grade=? WHERE student_id=? AND semester_id=? AND discipline_name=?",
                    (status, with_grade, grade, student_id, semester_id, discipline_name))
                self.connection.commit()
                return 2  # Updated existing exam

            else:
                # Insert the new exam
                self.cursor.execute(
                    "INSERT INTO StudentExams (student_id, semester_id, status, with_grade, grade, discipline_name) VALUES (?, ?, ?, ?, ?, ?)",
                    (student_id, semester_id, status, with_grade, grade, discipline_name))
                self.connection.commit()
                return 1  # Inserted new exam

        except sqlite3.Error:
            return 0  # Error

    def insert_department(self, name):
        self.cursor.execute(f'SELECT COUNT(*) FROM Departments WHERE name = "{name}"')
        exists = self.cursor.fetchone()['COUNT(*)']
        if exists:
            return 0
        else:
            self.cursor.execute(
                f'INSERT INTO Departments (name) VALUES ("{name}")')
            self.connection.commit()
            return 1

    def insert_major(self, name):
        self.cursor.execute(f'SELECT COUNT(*) FROM Majors WHERE name = "{name}"')
        exists = self.cursor.fetchone()['COUNT(*)']
        if exists:
            return 0
        else:
            self.cursor.execute(
                f'INSERT INTO Majors (name) VALUES ("{name}")')
            self.connection.commit()
            return 1

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