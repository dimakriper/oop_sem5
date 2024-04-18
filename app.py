import tkinter as tk
from tkinter import ttk

from store import Store


class StudentTableApp(tk.Tk):
    def __init__(self, data):
        super().__init__()
        self.title("Учёт успеваемости на факультете")
        self.data = data
        self.filtered_students = self.data.students
        self.initialize_gui()

    def initialize_gui(self):
        # Filter options for majors and departments
        self.map_majors = {major.name: major.id for major in self.data.majors}
        self.map_departments = {department.name: department.id for department in self.data.departments}
        majors_names = ['Все'] + list(self.map_majors.keys())
        departments_names = ['Все'] + list(self.map_departments.keys())

        # Inline filtering widgets
        filter_frame = ttk.Frame(self)
        filter_frame.pack(pady=10)

        ttk.Label(filter_frame, text="Специальность:").grid(row=0, column=0, padx=5)
        self.major_combobox = ttk.Combobox(filter_frame, values=majors_names, state="readonly")
        self.major_combobox.grid(row=0, column=1, padx=5)
        self.major_combobox.current(0)  # Set default selection to 'All'
        self.major_combobox.bind("<<ComboboxSelected>>", self.filter_data)

        ttk.Label(filter_frame, text="Факультет:").grid(row=0, column=2, padx=5)
        self.dept_combobox = ttk.Combobox(filter_frame, values=departments_names, state="readonly")
        self.dept_combobox.grid(row=0, column=3, padx=5)
        self.dept_combobox.current(0)  # Set default selection to 'All'
        self.dept_combobox.bind("<<ComboboxSelected>>", self.filter_data)

        # Table to display student data
        columns = ['Студент', 'Специальность', 'Факультет']
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=20)

        # Insert initial data into the table
        self.update_table(self.filtered_students)

    def filter_data(self, event=None):
        selected_major_name = self.major_combobox.get()
        selected_department_name = self.dept_combobox.get()

        self.filtered_students = [student for student in self.data.students
                                  if (selected_major_name == 'Все' or student.major_id == self.map_majors[selected_major_name])
                                  and (selected_department_name == 'Все' or student.department_id == self.map_departments[selected_department_name])
                                       ]

        self.update_table(self.filtered_students)
 
    def update_table(self, filtered_students):
        # Clear existing table data
        self.tree.delete(*self.tree.get_children())

        # Insert filtered data into the table
        for student in filtered_students:
            self.tree.insert('', 'end', values=(student.full_name,
                                                self.data.major_with_id(student.major_id).name,
                                                self.data.department_with_id(student.department_id).name
                                                )
                             )


if __name__ == "__main__":
    store = Store()
    app = StudentTableApp(store)
    app.mainloop()

