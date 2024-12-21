DELIMITER //

CREATE PROCEDURE RegisterCourse(
    IN p_name VARCHAR(200),          -- 강의 이름
    IN p_professor_id BIGINT,        -- 교수 ID
    IN p_classroom_id BIGINT,        -- 강의실 ID
    IN p_semester_id BIGINT,         -- 학기 ID
    IN p_max_students INT,           -- 최대 학생 수
    IN p_start_time TIME,            -- 강의 시작 시간
    IN p_end_time TIME               -- 강의 종료 시간
)
BEGIN
    -- 강의실 수용 가능 인원 확인
    DECLARE v_capacity INT;

    SELECT capacity 
    INTO v_capacity
    FROM Classrooms
    WHERE id = p_classroom_id;

    IF p_max_students > v_capacity THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Max students exceed classroom capacity';
    END IF;

    -- 강의실 및 시간 중복 확인
    IF EXISTS (
        SELECT 1
        FROM Courses c
        WHERE c.classroom_id = p_classroom_id
          AND c.semester_id = p_semester_id
          AND (
              (p_start_time BETWEEN c.start_time AND c.end_time) OR
              (p_end_time BETWEEN c.start_time AND c.end_time) OR
              (c.start_time BETWEEN p_start_time AND p_end_time) OR
              (c.end_time BETWEEN p_start_time AND p_end_time)
          )
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Classroom and time conflict with an existing course';
    END IF;

    -- 강의 등록
    INSERT INTO Courses (name, professor_id, classroom_id, semester_id, max_students, start_time, end_time)
    VALUES (p_name, p_professor_id, p_classroom_id, p_semester_id, p_max_students, p_start_time, p_end_time);
END //

DELIMITER ;
