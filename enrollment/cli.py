import mysql.connector
from datetime import datetime
from typing import Optional
import os
from prettytable import PrettyTable
import getpass
import time

from enrollment import CourseEnrollmentSystem


class ColorText:
    # Text colors
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    # Text styles
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    # End color
    END = '\033[0m'



class CourseEnrollmentCLI:
    def __init__(self):
        self.db = CourseEnrollmentSystem(
            host="localhost",
            user="root",
            password="root",
            database="CHOI"
        )
        self.current_student_id = None
        self.current_semester = None
        self.current_student_info = None

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self, text: str):
        print(f"\n{ColorText.HEADER}{ColorText.BOLD}=== {text} ==={ColorText.END}\n")

    def print_student_info(self):
        if self.current_student_info:
            info = self.current_student_info
            print(f"{ColorText.BLUE}{ColorText.BOLD}Student Information:{ColorText.END}")
            print(f"Name: {info['name']}")
            print(f"Department: {info['department_name']}")
            print(f"Email: {info['email']}")
            print(f"Phone: {info['phone_number']}\n")

    def display_courses(self, courses: list):
        table = PrettyTable()
        table.field_names = ["ID", "Course Name", "Professor", "Location", "Enrollment", "Status"]

        for course in courses:
            enrollment = f"{course['enrolled_students']}/{course['max_students']}"
            status = (ColorText.GREEN + "Available" + ColorText.END
                      if course['enrolled_students'] < course['max_students']
                      else ColorText.RED + "Full" + ColorText.END)

            table.add_row([
                course['id'],
                course['course_name'],
                course['professor_name'],
                f"{course['building_name']} {course['classroom_name']}",
                enrollment,
                status
            ])

        print(table)

    def display_enrollments(self, enrollments: list):
        table = PrettyTable()
        table.field_names = ["Enrollment Id", "Course Name", "Professor", "Mileage", "Status", "Enrolled At"]

        for enrollment in enrollments:
            status = (ColorText.GREEN + "Enrolled" + ColorText.END
                      if enrollment['is_success']
                      else ColorText.RED + "Failed" + ColorText.END)

            table.add_row([
                enrollment['enrollment_id'],
                enrollment['course_name'],
                enrollment['professor_name'],
                enrollment['mileage'],
                status,
                enrollment['enrolled_at'].strftime('%Y-%m-%d %H:%M')
            ])

        print(table)

    def login(self) -> bool:
        self.clear_screen()
        self.print_header("Login")

        try:
            student_id = int(input("Enter Student ID: "))
            student_info = self.db.get_student_info(student_id)

            if student_info:
                self.current_student_id = student_id
                self.current_student_info = student_info
                self.current_semester = self.db.get_current_semester()
                print(f"\n{ColorText.GREEN}Login successful!{ColorText.END}")
                time.sleep(1)
                return True
            else:
                print(f"\n{ColorText.RED}Student not found!{ColorText.END}")
                time.sleep(1)
                return False

        except ValueError:
            print(f"\n{ColorText.RED}Invalid student ID!{ColorText.END}")
            time.sleep(1)
            return False

    def display_main_menu(self):
        while True:
            self.clear_screen()
            self.print_student_info()

            print(f"{ColorText.BOLD}Main Menu:{ColorText.END}")
            print("1. View Available Courses")
            print("2. View My Enrollments")
            print("3. Enroll in Course")
            print("4. Cancel Enrollment")
            print("5. Logout")

            choice = input("\nEnter your choice (1-5): ")

            if choice == "1":
                self.view_available_courses()
            elif choice == "2":
                self.view_my_enrollments()
            elif choice == "3":
                self.enroll_in_course()
            elif choice == "4":
                self.cancel_enrollment()
            elif choice == "5":
                self.logout()
                break
            else:
                print(f"\n{ColorText.RED}Invalid choice!{ColorText.END}")
                time.sleep(1)

    def view_available_courses(self):
        self.clear_screen()
        self.print_header("Available Courses")

        if self.current_semester:
            courses = self.db.get_available_courses(self.current_semester['id'])
            self.display_courses(courses)
        else:
            print(f"{ColorText.RED}No active semester found!{ColorText.END}")

        input("\nPress Enter to continue...")

    def view_my_enrollments(self):
        self.clear_screen()
        self.print_header("My Enrollments")

        enrollments = self.db.get_student_enrollments(self.current_student_id)
        if enrollments:
            self.display_enrollments(enrollments)
        else:
            print("No enrollments found.")

        input("\nPress Enter to continue...")

    def enroll_in_course(self):
        self.clear_screen()
        self.print_header("Enroll in Course")

        # Display available courses first
        if self.current_semester:
            courses = self.db.get_available_courses(self.current_semester['id'])
            self.display_courses(courses)

            try:
                course_id = int(input("\nEnter Course ID: "))
                mileage = int(input("Enter Mileage: "))

                success, message = self.db.enroll_course(
                    self.current_student_id, course_id, mileage)

                if success:
                    print(f"\n{ColorText.GREEN}{message}{ColorText.END}")
                else:
                    print(f"\n{ColorText.RED}{message}{ColorText.END}")

            except ValueError:
                print(f"\n{ColorText.RED}Invalid input!{ColorText.END}")
        else:
            print(f"{ColorText.RED}No active semester found!{ColorText.END}")

        input("\nPress Enter to continue...")

    def cancel_enrollment(self):
        self.clear_screen()
        self.print_header("Cancel Enrollment")

        enrollments = self.db.get_student_enrollments(self.current_student_id)
        if enrollments:
            self.display_enrollments(enrollments)
            try:
                enrollment_id = int(input("\nEnter Enrollment ID to cancel: "))
                success, message = self.db.delete_enrollment(enrollment_id)
                if success:
                    print(f"\n{ColorText.GREEN}{message}{ColorText.END}")
                else:
                    print(f"\n{ColorText.RED}{message}{ColorText.END}")
            except ValueError:
                print(f"\n{ColorText.RED}Invalid input!{ColorText.END}")
        else:
            print(f"{ColorText.RED}No enrollments found!{ColorText.END}")

        input("\nPress Enter to continue...")

    def logout(self):
        self.current_student_id = None
        self.current_student_info = None
        self.current_semester = None
        print(f"\n{ColorText.BLUE}Logged out successfully!{ColorText.END}")
        time.sleep(1)

    def run(self):
        while True:
            if not self.current_student_id:
                if not self.login():
                    continue

            self.display_main_menu()

            if not self.current_student_id:  # After logout
                continue

            break

        self.db.close()


def main():
    try:
        cli = CourseEnrollmentCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
    finally:
        if hasattr(cli, 'db'):
            cli.db.close()


if __name__ == "__main__":
    main()
