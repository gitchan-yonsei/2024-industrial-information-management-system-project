import mysql.connector
from datetime import datetime
from typing import Optional


class CourseEnrollmentSystem:
    def __init__(self, host: str, user: str, password: str, database: str):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor(dictionary=True)

    def close(self):
        self.cursor.close()
        self.connection.close()

    def get_available_courses(self, semester_id: int) -> list:
        query = """
        SELECT 
            c.id,
            c.name as course_name,
            p.name as professor_name,
            c.max_students,
            cl.name as classroom_name,
            b.name as building_name,
            (
                SELECT COUNT(*) 
                FROM Enrollments e 
                WHERE e.course_id = c.id AND e.is_success = TRUE
            ) as enrolled_students
        FROM Courses c
        JOIN Professors p ON c.professor_id = p.id
        JOIN Classrooms cl ON c.classroom_id = cl.id
        JOIN Buildings b ON cl.building_id = b.id
        WHERE c.semester_id = %s
        """
        self.cursor.execute(query, (semester_id,))
        return self.cursor.fetchall()

    def get_student_enrollments(self, student_id: int) -> list:
        query = """
        SELECT 
            e.id as enrollment_id,
            c.name as course_name,
            p.name as professor_name,
            e.mileage,
            e.is_success,
            e.enrolled_at
        FROM Enrollments e
        JOIN Courses c ON e.course_id = c.id
        JOIN Professors p ON c.professor_id = p.id
        WHERE e.student_id = %s
        ORDER BY e.enrolled_at DESC
        """
        self.cursor.execute(query, (student_id,))
        return self.cursor.fetchall()

    def get_student_info(self, student_id: int) -> Optional[dict]:
        query = """
        SELECT 
            s.*,
            d.name as department_name
        FROM Students s
        JOIN Departments d ON s.department_id = d.id
        WHERE s.id = %s
        """
        self.cursor.execute(query, (student_id,))
        return self.cursor.fetchone()

    def get_current_semester(self) -> Optional[dict]:
        query = """
        SELECT id, year, term, starts_at, ends_at
        FROM Semesters
        WHERE starts_at <= CURDATE() AND ends_at >= CURDATE()
        LIMIT 1
        """
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def enroll_course(self, student_id: int, course_id: int, mileage: int) -> tuple[bool, str]:
        try:
            # Check if student already enrolled
            check_query = """
            SELECT id FROM Enrollments 
            WHERE student_id = %s AND course_id = %s AND is_success = TRUE
            """
            self.cursor.execute(check_query, (student_id, course_id))
            if self.cursor.fetchone():
                return False, "Already enrolled in this course"

            # Check course availability
            course_info = self.check_course_availability(course_id)
            if not course_info:
                return False, "Course not found"

            if course_info['current_enrollment'] >= course_info['max_students']:
                return False, "Course is full"

            # Insert enrollment
            insert_query = """
            INSERT INTO Enrollments 
                (student_id, course_id, mileage, is_success, enrolled_at)
            VALUES 
                (%s, %s, %s, TRUE, %s)
            """
            self.cursor.execute(insert_query,
                                (student_id, course_id, mileage, datetime.now()))
            self.connection.commit()
            return True, "Successfully enrolled"

        except mysql.connector.Error as err:
            self.connection.rollback()
            return False, f"Database error: {str(err)}"

    def delete_enrollment(self, enrollment_id: int) -> tuple[bool, str]:
        try:
            delete_query = """
            DELETE FROM Enrollments
            WHERE id = %s
            """
            self.cursor.execute(delete_query, (enrollment_id,))
            self.connection.commit()
            return True, "Successfully deleted enrollment"
        except mysql.connector.Error as err:
            self.connection.rollback()
            return False, f"Database error: {str(err)}"

    def check_course_availability(self, course_id: int) -> Optional[dict]:
        query = """
        SELECT 
            c.*,
            (
                SELECT COUNT(*) 
                FROM Enrollments e 
                WHERE e.course_id = c.id AND e.is_success = TRUE
            ) as current_enrollment
        FROM Courses c
        WHERE c.id = %s
        """
        self.cursor.execute(query, (course_id,))
        return self.cursor.fetchone()
