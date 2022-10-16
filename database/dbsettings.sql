-- Active: 1665006272340@@127.0.0.1@3306@db_emotions
CREATE TABLE IF NOT EXISTS EMPLEADO_EMOTIONS(id int NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key', create_time DATETIME COMMENT 'Create Time', name VARCHAR(255), emotion VARCHAR(255));

INSERT INTO EMPLEADO_EMOTIONS (create_time, name, emotion) VALUES ("2023/02/05", 'Test_empleado', 'Test_emotion')
