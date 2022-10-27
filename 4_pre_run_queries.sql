CREATE DATABASE bank_management_system;
USE bank_management_system;
CREATE TABLE employee_details (
    employee_id INT AUTO_INCREMENT,
    designation VARCHAR(10),
    name VARCHAR(100),
    email_id VARCHAR(50) UNIQUE,
    password VARCHAR(50),
    PRIMARY KEY (employee_id)
);
DESC employee_details;
INSERT INTO employee_details(employee_id,designation,name,email_id,password) VALUES(50000,"manager","manager1","manager1@gmail.com","manager1");
INSERT INTO employee_details(designation,name,email_id,password) VALUES("clerk","clerk1","clerk1@gmail.com","clerk1");
CREATE TABLE user_details (
    cif_id INT AUTO_INCREMENT,
    account_no INT UNIQUE,
    name VARCHAR(100),
    email_id VARCHAR(50) UNIQUE,
    password VARCHAR(50),
    PRIMARY KEY (cif_id)
);
INSERT INTO user_details(cif_id,account_no,name,email_id,password) VALUES(70000,10000,"user1","user1@gmail.com","user1");
INSERT INTO user_details(account_no,name,email_id,password) VALUES(10001,"user2","user2@gmail.com","user2");
CREATE TABLE transaction_details (
    employee_id INT,
    cif_id INT,
    account_no INT,
    transaction_id INT AUTO_INCREMENT,
    date DATE,
    date_and_time TIMESTAMP,
    debit FLOAT,
    credit FLOAT,
    remarks VARCHAR(50),
    balance FLOAT,
    PRIMARY KEY (transaction_id)
);
INSERT INTO transaction_details(employee_id, cif_id, account_no, transaction_id,date,date_and_time,debit,credit,remarks, balance) VALUES(50001,70000,10000,1000,now(),current_timestamp(),0,500,"by clerk",500);
INSERT INTO transaction_details(employee_id, cif_id, account_no, transaction_id,date,date_and_time,debit,credit,remarks, balance) VALUES(50001,70001,10001,1001,now(),current_timestamp(),0,500,"by clerk",500);
SELECT 
    *
FROM
    employee_details;
SELECT 
    *
FROM
    user_details;
SELECT 
    *
FROM
    transaction_details;