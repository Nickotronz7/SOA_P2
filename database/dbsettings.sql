-- Active: 1665102474961@@127.0.0.1@3306@db_emotions
CREATE TABLE EMPLEADO_EMOTIONS(  
    id int NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
    create_time DATETIME COMMENT 'Create Time',
    name VARCHAR(255),
    emotion VARCHAR(255)
) COMMENT '';

INSERT INTO EMPLEADO_EMOTIONS (create_time, name, emotion) VALUES ("2006-12-31 13:25:55", 'Test_empleado', 'Test_emotion')
