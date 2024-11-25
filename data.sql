INSERT INTO Departments (name)
VALUES ('컴퓨터공학과'),
       ('전자공학과'),
       ('산업공학과'),
       ('경영학과'),
       ('심리학과');

INSERT INTO Professors (name, department_id, email)
VALUES ('김철수', 1, 'kimcs@yonsei.ac.kr'),
       ('이영희', 2, 'leeyh@yonsei.ac.kr'),
       ('박민수', 3, 'parkms@yonsei.ac.kr'),
       ('최지현', 4, 'choijh@yonsei.ac.kr'),
       ('정하영', 5, 'junghy@yonsei.ac.kr');

INSERT INTO Students (name, email, phone_number, department_id)
VALUES ('홍길동', 'honggd@yonsei.ac.kr', '010-1234-5678', 1),
       ('김영수', 'kimys@yonsei.ac.kr', '010-2345-6789', 2),
       ('박지민', 'parkjm@yonsei.ac.kr', '010-3456-7890', 3),
       ('최유리', 'choiyr@yonsei.ac.kr', '010-4567-8901', 4),
       ('정수빈', 'jungsb@yonsei.ac.kr', '010-5678-9012', 5);

INSERT INTO Buildings (name)
VALUES ('백양관'),
       ('공학관'),
       ('상경관'),
       ('교육관'),
       ('법학관');

INSERT INTO Classrooms (name, building_id, capacity)
VALUES ('101호', 1, 50),
       ('202호', 2, 60),
       ('303호', 3, 40),
       ('404호', 4, 70),
       ('505호', 5, 30);

INSERT INTO Semesters (year, term, starts_at, ends_at)
VALUES (2024, 'Spring', '2024-03-01', '2024-06-30'),
       (2024, 'Summer', '2024-07-01', '2024-08-31'),
       (2024, 'Fall', '2024-09-01', '2024-12-31'),
       (2025, 'Winter', '2025-01-01', '2025-02-28');

INSERT INTO Courses (name, professor_id, classroom_id, semester_id, max_students)
VALUES ('자료구조', 1, 1, 1, 50),
       ('전자회로', 2, 2, 1, 60),
       ('생산관리', 3, 3, 2, 40),
       ('마케팅', 4, 4, 3, 70),
       ('사회심리학', 5, 5, 4, 30);

INSERT INTO Enrollments (student_id, course_id, mileage, is_success)
VALUES (1, 1, 50, TRUE),
       (2, 2, 40, TRUE),
       (3, 3, 30, TRUE),
       (4, 4, 60, TRUE),
       (5, 5, 20, TRUE),
       (1, 2, 10, FALSE),
       (2, 3, 15, FALSE);
