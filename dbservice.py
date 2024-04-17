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
        # Assuming you have a cursor object connected to your database

        # Define the SQL query with a JOIN between StudentExams and Disciplines tables
        query = f"""
            SELECT StudentExams.*, Disciplines.name 
            FROM StudentExams 
            INNER JOIN Disciplines 
            ON StudentExams.discipline_id = Disciplines.id 
            WHERE StudentExams.student_id = {student_id}
        """

        # Execute the SQL query
        self.cursor.execute(query)

        # Fetch all the rows from the result
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

