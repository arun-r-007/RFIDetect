CREATE DATABASE attendance_system;

USE attendance_system;

CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    rfid_tag VARCHAR(50),
    face_encoding LONGBLOB
);


drop table Users;

select * from Users;

SET SQL_SAFE_UPDATES = 0;
SET SQL_SAFE_UPDATES = 1;


DELETE FROM Users WHERE rfid_tag = '12ad34';


CREATE TABLE Attendance (
    record_id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(50) NOT NULL,
    rfid_tag VARCHAR(50) NOT NULL,
    period INT NOT NULL, -- Add the period column
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) NOT NULL CHECK (status IN ('Present', 'Absent', 'Frozen'))
);



select * from Attendance;


drop table Attendance;

DELETE FROM Attendance WHERE rfid_tag = '12ad34' and status ='Absent' ;

INSERT INTO Attendance (user_name, rfid_tag, timestamp, status)
VALUES('Name', '12ad34', '2024-12-11 15:00:00', 'Present');




SELECT user, host, plugin FROM mysql.user WHERE user = 'root';

ALTER TABLE Users MODIFY face_encoding LONGBLOB;