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

def get_all_student_courses():
    conn = connect_db()
    cursor = conn.cursor()
    
    # 모든 학생의 student_id 조회
    cursor.execute("SELECT id FROM Students")
    
    # 각 학생에 대해 수강 정보를 출력
    for (student_id,) in cursor.fetchall():
        print(f"학생 ID: {student_id}의 수강 강의:")
        cursor.execute("SELECT get_student_courses_function(%s)", (student_id,))
        
        # 수강 정보 출력
        for (result,) in cursor.fetchall():
            print(result)
        print("-" * 40)  # 구분선
    
    cursor.close()
    conn.close()


def main_menu():
    while True:
        print("\n--- 수강신청 분석 시스템 ---")
        print("1. 각 강의별 평균 신청 마일리지")
        print("2. 각 강의별 수강신청에 성공한 신청의 평균 마일리지")
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
            get_all_student_courses()
        elif choice == '5':
            print("프로그램을 종료합니다.")
            break
        else:
            print("올바른 메뉴를 선택하세요.")

if __name__ == "__main__":
    main_menu()
