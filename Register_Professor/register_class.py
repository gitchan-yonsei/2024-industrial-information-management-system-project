import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import time

class ProfessorCourseRegistrationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Professor Course Registration")
        self.root.geometry("600x400")

        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="CHOI"
        )
        self.cursor = self.db.cursor(dictionary=True)

        self.setup_gui()

    def setup_gui(self):
        input_frame = ttk.Frame(self.root, padding=10)
        input_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(input_frame, text="Course Name:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.course_name_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.course_name_var).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Professor ID:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.professor_id_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.professor_id_var).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Classroom ID:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.classroom_id_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.classroom_id_var).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Semester ID:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.semester_id_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.semester_id_var).grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Max Students:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.max_students_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.max_students_var).grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Start Time (HH:MM):").grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        self.start_time_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.start_time_var).grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="End Time (HH:MM):").grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
        self.end_time_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.end_time_var).grid(row=6, column=1, padx=5, pady=5)

        ttk.Button(input_frame, text="Register Course", command=self.register_course).grid(row=7, column=0, columnspan=2, pady=10)

    def register_course(self):
        try:

            course_name = self.course_name_var.get()
            professor_id = int(self.professor_id_var.get())
            classroom_id = int(self.classroom_id_var.get())
            semester_id = int(self.semester_id_var.get())
            max_students = int(self.max_students_var.get())
            start_time = self.parse_time(self.start_time_var.get())
            end_time = self.parse_time(self.end_time_var.get())


            query = "CALL RegisterCourse(%s, %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(query, (course_name, professor_id, classroom_id, semester_id, max_students, start_time, end_time))
            self.db.commit()

            messagebox.showinfo("Success", "Course registered successfully!")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid input values.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def parse_time(self, time_str):
        try:
            hours, minutes = map(int, time_str.split(':'))
            return time(hours, minutes)
        except ValueError:
            raise ValueError("Invalid time format. Please use HH:MM format.")

    def close_connection(self):
        self.cursor.close()
        self.db.close()

def main():
    root = tk.Tk()
    app = ProfessorCourseRegistrationApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close_connection)  # Close DB connection on exit
    root.mainloop()

if __name__ == "__main__":
    main()
