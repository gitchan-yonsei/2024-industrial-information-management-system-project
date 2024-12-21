CREATE VIEW ProfessorCoursesView AS
SELECT 
    p.name AS professor_name,
    c.name AS course_name,
    s.year,
    s.term
FROM Courses c
JOIN Professors p ON c.professor_id = p.id
JOIN Semesters s ON c.semester_id = s.id;
