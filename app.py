import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from store import Store
from models.exams import *


class ExamCreateWindow(tk.Toplevel):
    def __init__(self, parent, student):
        super().__init__(parent)
        self.parent = parent
        self.title('Новый экзамен')
        self.geometry("300x300")
        self.student = student
        self.statuses = {'-': 0, 'Не сдан (незачет)': 1, 'Сдан (зачет)': 2}
        self.grades = {'-': None, 'неуд.': 2, 'удовл.' : 3, 'хорошо' : 4, 'отлично': 5}
        self.initialize_gui()

    def initialize_gui(self):
        ttk.Label(self, text=self.student.full_name).pack(pady=3)
        self.semester_combobox = SemesterSelectWidget(self)
        self.semester_combobox.current(0)
        self.semester_combobox.pack(pady=3)

        ttk.Label(self, text="Название дисциплины:").pack()
        self.name_entry = ttk.Entry(self)
        self.name_entry.pack()

        ttk.Label(self, text="Статус экзамена:").pack()
        self.status_combobox = ttk.Combobox(self, values=list(self.statuses.keys()), state='readonly')
        self.status_combobox.current(0)
        self.status_combobox.pack()

        ttk.Label(self, text="Оценка:").pack()
        self.grade_combobox = ttk.Combobox(self, values=list(self.grades.keys()), state='readonly')
        self.grade_combobox.current(0)
        self.grade_combobox.pack()

        ttk.Button(self,
                   text='Создать',
                   command=self.create_exam).pack(pady=5)

    def create_exam(self):
        sem_id = self.semester_combobox.map_semesters[self.semester_combobox.get()]
        name = self.name_entry.get()
        sts = self.statuses[self.status_combobox.get()]
        grade = self.grades[self.grade_combobox.get()]
        with_grade = 0 if not grade else 1
        if not name :
            messagebox.showwarning("Предупреждение", "Пожалуйста, заполните название дисциплины")
            return
        Store()._db_service.insert_exam(student_id=self.student.id,
                                        semester_id=sem_id,
                                        status=sts,
                                        grade=grade,
                                        with_grade=with_grade,
                                        discipline_name=name
                                        )

        Store()._load_students()
        self.destroy()





class StudentReportWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Отчет об успеваемости')
        self.geometry("300x200")
    def show_report(self, student = None):

        for widget in self.winfo_children():
            widget.destroy()
        ttk.Label(self, text=student.full_name).pack()

        self.semester_combobox = SemesterSelectWidget(self, student)
        self.semester_combobox.pack(pady=3)


        def get_semester_results(event=None):
            for widget in self.report_frame.winfo_children():
                widget.destroy()
            sem_id = self.semester_combobox.map_semesters[self.semester_combobox.get()]
            ttk.Label(self.report_frame, text=f'Средний балл: {student.average_grade(sem_id)}').grid()

            row_index = 1
            for exam in student.exams(sem_id):
                label_text = f'{exam.discipline_name}: {exam.status_str}'
                label = ttk.Label(self.report_frame, text=label_text)
                label.grid(row=row_index, column=0, sticky='w', padx=5)
                delete_button = ttk.Button(self.report_frame, text="Delete",
                                           command=lambda exam_id=exam.id: delete_exam(exam_id))
                delete_button.grid(row=row_index, column=1, sticky='w', padx=5)
                row_index += 1
            def delete_exam(exam_id):
                Store()._db_service.delete_exam(exam_id)
                Store()._load_students()
                messagebox.showinfo("", "Экзамен удален")
                self.destroy()


        self.semester_combobox.bind("<<ComboboxSelected>>", get_semester_results)


        self.report_frame = ttk.Frame(self)
        self.report_frame.pack()

class StudentCreateWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title('Новый студент')
        self.geometry("300x300")

        self.dept_combobox = DepartmentSelectWidget(self)
        ttk.Label(self, text="Факультет:").pack()
        self.dept_combobox.pack()

        self.major_combobox = MajorSelectWidget(self)
        ttk.Label(self, text="Cпециальность:").pack()
        self.major_combobox.pack()

        ttk.Label(self, text="Имя:").pack()
        self.name_entry = ttk.Entry(self)
        self.name_entry.pack()

        ttk.Label(self, text="Фамилия:").pack()
        self.surname_entry = ttk.Entry(self)
        self.surname_entry.pack()

        ttk.Label(self, text="Отчество:").pack()
        self.patronym_entry = ttk.Entry(self)
        self.patronym_entry.pack()

        ttk.Button(self,
                   text='Новый студент',
                   command=self.create_student).pack(pady=5)

    def create_student(self):
        selected_major_name = self.major_combobox.get()
        selected_department_name = self.dept_combobox.get()
        major_id = self.major_combobox.map_majors[selected_major_name]
        department_id = self.dept_combobox.map_departments[selected_department_name]
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        patronym = self.patronym_entry.get()


        # Check if name and surname are filled
        if not name or not surname:
            messagebox.showwarning("Предупреждение", "Пожалуйста, заполните поля 'Имя' и 'Фамилия'.")
            return
        insert = Store()._db_service.insert_student(name, surname, patronym, department_id, major_id)
        if insert:
            messagebox.showinfo("","Студент успешно создан")
        else:
            messagebox.showwarning("","Не удалось создать студента")
        Store()._load_students()
        self.parent.filter_data()
        self.destroy()
class DepartmentSelectWidget(ttk.Combobox):
    def __init__(self, parent):
        self.map_departments = {department.name: department.id for department in Store().departments}
        departments_names = list(self.map_departments.keys())
        super().__init__(parent, values=departments_names, state="readonly")
        self.current(0)

class MajorSelectWidget(ttk.Combobox):
    def __init__(self, parent):
        self.map_majors = {major.name: major.id for major in Store().majors}
        majors_names = list(self.map_majors.keys())
        super().__init__(parent, values=majors_names, state="readonly")
        self.current(0)

class SemesterSelectWidget(ttk.Combobox):
    def __init__(self, parent, student=None):
        if not student:
            semesters = Store().semesters
        else:
            semesters = set([Store().semester_with_id(exam.semester_id) for exam in student.exams()])
        self.map_semesters = {s.name: s.id for s in semesters}

        semester_names = list(self.map_semesters.keys())

        super().__init__(parent, values=semester_names, state="readonly")


class StudentTableApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.resizable(False, False)
        self.title("Учёт успеваемости на факультете")
        self.filtered_students = Store().students
        self.initialize_gui()

    def initialize_gui(self):



        main_frame = ttk.Frame(self)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.dept_combobox = DepartmentSelectWidget(main_frame)
        ttk.Label(main_frame, text="Факультет:").grid(row=0, column=0, padx=5)
        self.dept_combobox.grid(row=1, column=0, padx=5)
        self.dept_combobox.bind("<<ComboboxSelected>>", self.filter_data)

        self.major_combobox = MajorSelectWidget(main_frame)
        ttk.Label(main_frame, text="Cпециальность:").grid(row=0, column=1, padx=5)
        self.major_combobox.grid(row=1, column=1, padx=5)
        self.major_combobox.bind("<<ComboboxSelected>>", self.filter_data)

        columns = ["", 'Студент', 'Специальность', 'Факультет']
        self.tree = ttk.Treeview(main_frame, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.grid(row=2, column=0, columnspan=4, pady=20)

        self.update_table(self.filtered_students)

        ttk.Label(main_frame, text="Выбирите студента из таблицы чтобы получить отчет об успеваемости").grid(row=3, pady=10)

        self.main_frame = main_frame
        separator = ttk.Separator(self, orient="vertical")
        separator.grid(row=0, column=1, sticky="ns", padx=10, pady=10)

        sidebar_frame = ttk.Frame(self)
        sidebar_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

        ttk.Button(sidebar_frame,
                   text='Новый студент',
                   command=self.open_student_create_window).pack()
        ttk.Button(sidebar_frame,
                   text="Удалить студента",
                   command=self.on_delete_student_button_click).pack()
        ttk.Button(sidebar_frame,
                   text="Успеваемость",
                   command=self.on_select_student).pack()
        ttk.Button(sidebar_frame,
                   text="Новый экзамен",
                   command=self.open_exam_create_window).pack()

    def filter_data(self, event=None):
        selected_major_name = self.major_combobox.get()
        selected_department_name = self.dept_combobox.get()

        self.filtered_students = [
            student for student in Store().students
            if (selected_major_name == 'Все' or student.major_id == self.major_combobox.map_majors[selected_major_name])
            and (selected_department_name == 'Все' or student.department_id == self.dept_combobox.map_departments[selected_department_name])
        ]

        self.update_table(self.filtered_students)

    def update_table(self, filtered_students):
        self.tree.delete(*self.tree.get_children())
        for student in filtered_students:
            self.tree.insert('', 'end', values=(
                student.id,
                student.full_name,
                Store().major_with_id(student.major_id).name,
                Store().department_with_id(student.department_id).name
            ))




    def on_select_student(self, Event=None):
        student = self._get_current_student()
        window = StudentReportWindow(self)
        window.grab_set()
        window.show_report(student)

    def open_student_create_window(self):
        window = StudentCreateWindow(self)
        window.grab_set()

    def delete_student(self, id):
        Store()._db_service.delete_student(id)
        Store()._load_students()
        self.filter_data()

    def open_exam_create_window(self):
        student = self._get_current_student()
        window = ExamCreateWindow(self, student)
        window.grab_set()


    def on_delete_student_button_click(self, Event=None):
        student = self._get_current_student()
        self.delete_student(student.id)

    def _get_current_student(self):
        selected_item = self.tree.focus()
        if selected_item:
            student_id = self.tree.item(selected_item)['values'][0]
            student = Store().student_with_id(student_id)
            return student
        else:
            messagebox.showwarning("Предупреждение", "Не выбран студент")

if __name__ == "__main__":
    store = Store()
    app = StudentTableApp()
    app.mainloop()
