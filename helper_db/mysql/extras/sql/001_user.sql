-- create database
CREATE DATABASE user;

-- use database
USE user;

-- create table
CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(50),
    gender VARCHAR(50),
    PRIMARY KEY(id));

-- insert dummy data in to table
INSERT INTO users (first_name, last_name, email, gender) VALUES ('Engracia', 'Gwyther', 'egwyther0@redcross.org', 'F');
INSERT INTO users (first_name, last_name, email, gender) VALUES ('Ximenez', 'MacNeachtain', 'xmacneachtain1@posterous.com', 'NS');
INSERT INTO users (first_name, last_name, email, gender) VALUES ('Fitzgerald', 'Hartus', 'fhartus2@cdbaby.com', 'M');
INSERT INTO users (first_name, last_name, email, gender) VALUES ('Beniamino', 'Beirne', 'bbeirne3@engadget.com', 'F');
INSERT INTO users (first_name, last_name, email, gender) VALUES ('Adriana', 'Armal', 'aarmal4@booking.com', 'NS');

-- get all records from the table
SELECT * FROM users;

-- sql procedures
-- CALL get_users()
DELIMITER &&
CREATE PROCEDURE get_users ()
BEGIN
SELECT * FROM users;
END &&
DELIMITER ;

-- CALL get_user_by_id(11)
DELIMITER &&
CREATE PROCEDURE get_user_by_id (IN U_id INT)
BEGIN
SELECT first_name, last_name, email, gender FROM users WHERE id = U_id;
END &&
DELIMITER ;

-- CALL insert_user('Jane','Doe','jane.doe@automation.com', 'M')
DELIMITER &&
Create PROCEDURE insert_user (IN U_first_name VARCHAR(50), IN U_last_name VARCHAR(50), IN U_email Varchar(50), IN U_gender Varchar(50))
BEGIN
INSERT INTO users (first_name, last_name, email, gender) VALUES (U_first_name, U_last_name, U_email, U_gender);
END &&
DELIMITER ;
