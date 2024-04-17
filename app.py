import tkinter as tk
from tkinter import ttk

from models.student import Student


class StudentTableApp(tk.Tk):
    def __init__(self, students):
        super().__init__()
        self.title("Student Table App")
        self.students = students
        self.filtered_students = students  # Initialize with all students
        self.initialize_gui()

    def initialize_gui(self):
        # Filter options for majors and departments
        majors = ['All'] + sorted(set(student.major for student in self.students))
        departments = ['All'] + sorted(set(student.department for student in self.students))

        # Inline filtering widgets
        filter_frame = ttk.Frame(self)
        filter_frame.pack(pady=10)

        ttk.Label(filter_frame, text="Filter by Major:").grid(row=0, column=0, padx=5)
        self.major_combobox = ttk.Combobox(filter_frame, values=majors, state="readonly")
        self.major_combobox.grid(row=0, column=1, padx=5)
        self.major_combobox.current(0)  # Set default selection to 'All'
        self.major_combobox.bind("<<ComboboxSelected>>", self.filter_data)

        ttk.Label(filter_frame, text="Filter by Department:").grid(row=0, column=2, padx=5)
        self.dept_combobox = ttk.Combobox(filter_frame, values=departments, state="readonly")
        self.dept_combobox.grid(row=0, column=3, padx=5)
        self.dept_combobox.current(0)  # Set default selection to 'All'
        self.dept_combobox.bind("<<ComboboxSelected>>", self.filter_data)

        # Table to display student data
        columns = ['Name', 'Major', 'Department']
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=20)

        # Insert initial data into the table
        self.update_table(self.filtered_students)

    def filter_data(self, event=None):
        selected_major = self.major_combobox.get()
        selected_department = self.dept_combobox.get()

        self.filtered_students = [student for student in self.students
                                  if (selected_major == 'All' or student.major == selected_major)
                                  and (selected_department == 'All' or student.department == selected_department)]

        self.update_table(self.filtered_students)
 
    def update_table(self, filtered_students):
        # Clear existing table data
        self.tree.delete(*self.tree.get_children())

        # Insert filtered data into the table
        for student in filtered_students:
            self.tree.insert('', 'end', values=(student.name, student.major, student.department))


if __name__ == "__main__":
    # Sample student data (replace this with your actual data)
    students = [
        Student("Alice", "Computer Science", "CS"),
        Student("Bob", "Engineering", "Engineering"),
        Student("Charlie", "Mathematics", "Math"),
        Student("David", "Physics", "Physics")
    ]

    # Create and run the tkinter app
    app = StudentTableApp(students)
    app.mainloop()

