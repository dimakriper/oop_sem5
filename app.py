import tkinter as tk
from tkinter import ttk
from store import Store
from models.exams import *

class StudentTableApp(tk.Tk):
    def __init__(self, data):
        super().__init__()
        self.resizable(False, False)
        self.title("Учёт успеваемости на факультете")
        self.data = data
        self.filtered_students = self.data.students
        self.initialize_gui()

    def initialize_gui(self):
        self.map_majors = {major.name: major.id for major in self.data.majors}
        self.map_departments = {department.name: department.id for department in self.data.departments}
        majors_names = ['Все'] + list(self.map_majors.keys())
        departments_names = ['Все'] + list(self.map_departments.keys())

        main_frame = ttk.Frame(self)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        ttk.Label(main_frame, text="Специальность:").grid(row=0, column=0, padx=5)
        self.major_combobox = ttk.Combobox(main_frame, values=majors_names, state="readonly")
        self.major_combobox.grid(row=0, column=1, padx=5)
        self.major_combobox.current(0)
        self.major_combobox.bind("<<ComboboxSelected>>", self.filter_data)

        ttk.Label(main_frame, text="Факультет:").grid(row=0, column=2, padx=5)
        self.dept_combobox = ttk.Combobox(main_frame, values=departments_names, state="readonly")
        self.dept_combobox.grid(row=0, column=3, padx=5)
        self.dept_combobox.current(0)
        self.dept_combobox.bind("<<ComboboxSelected>>", self.filter_data)



        columns = ["", 'Студент', 'Специальность', 'Факультет']
        self.tree = ttk.Treeview(main_frame, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.grid(row=1, column=0, columnspan=4, pady=20)

        self.tree.bind('<<TreeviewSelect>>', self.on_select_student)
        scrollbar = ttk.Scrollbar(orient='vertical', command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.update_table(self.filtered_students)

        separator = ttk.Separator(self, orient="vertical")
        separator.grid(row=0, column=1, sticky="ns", padx=10, pady=10)

        sidebar_frame = ttk.Frame(self)
        sidebar_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

        ttk.Label(self, text="Выбирите студента из таблицы чтобы получить отчет об успеваемости").grid(row=1, pady=10)

        self.main_frame = main_frame
        self.sidebar_frame = sidebar_frame

    def filter_data(self, event=None):
        selected_major_name = self.major_combobox.get()
        selected_department_name = self.dept_combobox.get()

        self.filtered_students = [
            student for student in self.data.students
            if (selected_major_name == 'Все' or student.major_id == self.map_majors[selected_major_name])
            and (selected_department_name == 'Все' or student.department_id == self.map_departments[selected_department_name])
        ]

        self.update_table(self.filtered_students)

    def update_table(self, filtered_students):
        self.tree.delete(*self.tree.get_children())
        for student in filtered_students:
            self.tree.insert('', 'end', values=(
                student.id,
                student.full_name,
                self.data.major_with_id(student.major_id).name,
                self.data.department_with_id(student.department_id).name
            ))

    def show_report(self, student = None):

        for widget in self.sidebar_frame.winfo_children():
            widget.destroy()
        ttk.Label(self.sidebar_frame, text=student.full_name).pack()

        semesters = set([self.data.semester_with_id(exam.semester_id) for exam in student.exams()])
        self.map_semesters = {s.name: s.id for s in semesters}

        semester_names = list(self.map_semesters.keys())

        def get_semester_results(event):
            for widget in self.report_frame.winfo_children():
                widget.destroy()
            sem_id = self.map_semesters[self.semester_combobox.get()]
            ttk.Label(self.report_frame, text=f'Средний балл: {student.average_grade(sem_id)}').pack()

            for exam in student.exams(sem_id):
                ttk.Label(self.report_frame, text=f'{exam.discipline_name}: {exam.status_str}').pack(fill='x')

        self.semester_combobox = ttk.Combobox(self.sidebar_frame, values=semester_names, state="readonly")
        self.semester_combobox.pack(pady=3)
        ttk.Separator(self.sidebar_frame, orient='horizontal').pack(pady=2)
        self.semester_combobox.bind("<<ComboboxSelected>>", get_semester_results)

        self.report_frame = ttk.Frame(self.sidebar_frame)
        self.report_frame.pack()




    def on_select_student(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            student_id = self.tree.item(selected_item)['values'][0]
            student = self.data.student_with_id(student_id)
            self.show_report(student)





if __name__ == "__main__":
    store = Store()
    app = StudentTableApp(store)
    app.mainloop()
