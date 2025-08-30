-- Create Database attendance_db;
-- Use attendance_db;

-- Create TABLE employee(
-- 	emp_id INT primary key auto_increment,
--     name varchar(20) NOT NULL,
--     dept varchar(20) NOT null
--     );

Select * from employee;
Select * from attendance;

-- CREATE TABLE attendance (
-- 	id INT primary key auto_increment,
--     emp_id INT,
--     date DATE,
--     status ENUM('Present','Absent'),
--     Foreign Key(emp_id) references employee(emp_id)
--     );
    