import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mydb"
    )

def get_avg_mileage():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            c.name AS course_name,
            p.name AS professor_name,
            AVG(e.mileage) AS avg_mileage
        FROM Enrollments e
        JOIN Courses c ON e.course_id = c.id
        JOIN Professors p ON c.professor_id = p.id
        GROUP BY c.name, p.name
    """)
    for course_name, professor_name, avg_mileage in cursor.fetchall():
        print(f"강의: {course_name}, 교수: {professor_name}, 평균 마일리지: {avg_mileage:.2f}")
    cursor.close()
    conn.close()

def get_avg_successful_mileage():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            c.name AS course_name,
            p.name AS professor_name,
            AVG(e.mileage) AS avg_successful_mileage
        FROM Enrollments e
        JOIN Courses c ON e.course_id = c.id
        JOIN Professors p ON c.professor_id = p.id
        WHERE e.is_success = TRUE
        GROUP BY c.name, p.name
    """)
    for course_name, professor_name, avg_mileage in cursor.fetchall():
        print(f"강의: {course_name}, 교수: {professor_name}, 성공한 수강생 평균 마일리지: {avg_mileage:.2f}")
    cursor.close()
    conn.close()

def get_professor_courses():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            p.name AS professor_name,
            c.name AS course_name,
            s.year,
            s.term
        FROM Courses c
        JOIN Professors p ON c.professor_id = p.id
        JOIN Semesters s ON c.semester_id = s.id
        ORDER BY p.name, s.year, s.term
    """)
    for professor_name, course_name, year, term in cursor.fetchall():
        print(f"교수: {professor_name}, 강의: {course_name}, 학기: {year} {term}")
    cursor.close()
    conn.close()

def get_student_courses():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            s.name AS student_name,
            c.name AS course_name,
            p.name AS professor_name,
            sem.year,
            sem.term
        FROM Enrollments e
        JOIN Students s ON e.student_id = s.id
        JOIN Courses c ON e.course_id = c.id
        JOIN Professors p ON c.professor_id = p.id
        JOIN Semesters sem ON c.semester_id = sem.id
        WHERE e.is_success = TRUE
        ORDER BY s.name, sem.year, sem.term
    """)
    for student_name, course_name, professor_name, year, term in cursor.fetchall():
        print(f"학생: {student_name}, 강의: {course_name}, 교수: {professor_name}, 학기: {year} {term}")
    cursor.close()
    conn.close()

def main_menu():
    while True:
        print("\n--- 수강신청 분석 시스템 ---")
        print("1. 각 강의별 평균 신청 마일리지")
        print("2. 각 강의별 수강신청에 성공한 신청의 평균 신청 마일리지")
        print("3. 교수별 진행하는 강의 조회")
        print("4. 학생별 수강 성공한 강의 조회")
        print("5. 종료")
        
        choice = input("메뉴를 선택하세요: ")
        
        if choice == '1':
            get_avg_mileage()
        elif choice == '2':
            get_avg_successful_mileage()
        elif choice == '3':
            get_professor_courses()
        elif choice == '4':
            get_student_courses()
        elif choice == '5':
            print("프로그램을 종료합니다.")
            break
        else:
            print("올바른 메뉴를 선택하세요.")

if __name__ == "__main__":
    main_menu()
