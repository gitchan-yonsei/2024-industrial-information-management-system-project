DELIMITER $$

CREATE FUNCTION get_student_courses_function(student_id BIGINT)
RETURNS VARCHAR(2000)
DETERMINISTIC
BEGIN
    DECLARE result VARCHAR(2000);
    SET result = '';

    -- 수강 신청에 성공한 강의 정보들을 가져오기
    SELECT GROUP_CONCAT(CONCAT(
                '강의: ', c.name, ', ',
                '교수: ', p.name, ', ',
                '학기: ', sem.year, ' ', sem.term
            ) SEPARATOR '\n')
    INTO result
    FROM Enrollments e
    JOIN Students s ON e.student_id = s.id
    JOIN Courses c ON e.course_id = c.id
    JOIN Professors p ON c.professor_id = p.id
    JOIN Semesters sem ON c.semester_id = sem.id
    WHERE e.is_success = TRUE AND s.id = student_id;

    RETURN result;
END$$

DELIMITER ;
