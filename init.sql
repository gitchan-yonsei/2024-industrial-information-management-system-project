-- 학과 테이블: 학과의 기본 정보 저장
CREATE TABLE Departments
(
    id   BIGINT AUTO_INCREMENT PRIMARY KEY, -- 학과 고유 식별자
    name VARCHAR(100) NOT NULL              -- 학과 이름 (예: 산업공학과)
);

-- 교수 테이블 수정: 교수의 기본 정보 저장
CREATE TABLE Professors
(
    id            BIGINT AUTO_INCREMENT PRIMARY KEY,        -- 교수 고유 식별자
    name          VARCHAR(100)        NOT NULL,             -- 교수 이름
    department_id BIGINT              NOT NULL,             -- 소속 학과 ID (Departments 테이블 참조)
    email         VARCHAR(200) UNIQUE NOT NULL,             -- 교수 이메일 (유니크)
    FOREIGN KEY (department_id) REFERENCES Departments (id) -- 학과 외래 키
);

-- 학생 테이블 수정: 학생의 기본 정보 저장
CREATE TABLE Students
(
    id            BIGINT AUTO_INCREMENT PRIMARY KEY,        -- 학생 고유 식별자
    name          VARCHAR(100)        NOT NULL,             -- 학생 이름
    email         VARCHAR(200) UNIQUE NOT NULL,             -- 학생 이메일 (유니크)
    phone_number  VARCHAR(20),                              -- 학생 연락처
    department_id BIGINT              NOT NULL,             -- 소속 학과 ID (Departments 테이블 참조)
    FOREIGN KEY (department_id) REFERENCES Departments (id) -- 학과 외래 키
);


-- 건물 테이블: 강의실이 속한 건물 정보를 저장
CREATE TABLE Buildings
(
    id   BIGINT AUTO_INCREMENT PRIMARY KEY, -- 건물 고유 식별자
    name VARCHAR(100) NOT NULL              -- 건물 이름
);

-- 강의실 테이블: 강의실의 기본 정보를 저장
CREATE TABLE Classrooms
(
    id          BIGINT AUTO_INCREMENT PRIMARY KEY,      -- 강의실 고유 식별자
    name        VARCHAR(100) NOT NULL,                  -- 강의실 이름
    building_id BIGINT       NOT NULL,                  -- 건물 ID (Buildings 테이블 참조)
    capacity    INT          NOT NULL,                  -- 강의실 수용 가능 인원
    FOREIGN KEY (building_id) REFERENCES Buildings (id) -- 건물 외래 키
);

-- 학기 테이블: 학기 정보를 저장 (연도와 학기)
CREATE TABLE Semesters
(
    id        BIGINT AUTO_INCREMENT PRIMARY KEY, -- 학기 고유 식별자
    year      INT         NOT NULL,              -- 연도 (예: 2024)
    term      VARCHAR(10) NOT NULL,              -- 학기 구분 ('Spring', 'Summer', 'Fall', 'Winter')
    starts_at DATE        NOT NULL,              -- 학기 시작일
    ends_at   DATE        NOT NULL,              -- 학기 종료일
    UNIQUE (year, term)
);

-- 수업 테이블: 개설된 수업 정보를 저장
CREATE TABLE Courses
(
    id           BIGINT AUTO_INCREMENT PRIMARY KEY,        -- 수업 고유 식별자
    name         VARCHAR(200) NOT NULL,                    -- 수업 이름 (예: 데이터베이스 기초)
    professor_id BIGINT       NOT NULL,                    -- 담당 교수 ID (Professors 테이블 참조)
    classroom_id BIGINT       NOT NULL,                    -- 강의실 ID (Classrooms 테이블 참조)
    semester_id  BIGINT       NOT NULL,                    -- 학기 ID (Semesters 테이블 참조)
    max_students INT          NOT NULL,                    -- 수업 최대 수강 가능 인원 (강의실 capacity보다 작아야 함)
    FOREIGN KEY (professor_id) REFERENCES Professors (id), -- 교수 외래 키
    FOREIGN KEY (classroom_id) REFERENCES Classrooms (id), -- 강의실 외래 키
    FOREIGN KEY (semester_id) REFERENCES Semesters (id)    -- 학기 외래 키
);

-- 수강 신청 테이블: 학생의 수강 신청 정보를 저장
CREATE TABLE Enrollments
(
    id          BIGINT AUTO_INCREMENT PRIMARY KEY,     -- 수강 신청 고유 식별자
    student_id  BIGINT NOT NULL,                       -- 신청 학생 ID (Students 테이블 참조)
    course_id   BIGINT NOT NULL,                       -- 신청한 수업 ID (Courses 테이블 참조)
    mileage     INT    NOT NULL,                       -- 수강 신청에 사용한 마일리지
    is_success  BOOLEAN  DEFAULT FALSE,                -- 수강 성공 여부 (TRUE/FALSE)
    enrolled_at DATETIME DEFAULT CURRENT_TIMESTAMP,    -- 수강 신청 시간
    FOREIGN KEY (student_id) REFERENCES Students (id), -- 학생 외래 키
    FOREIGN KEY (course_id) REFERENCES Courses (id)    -- 수업 외래 키
);
