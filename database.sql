CREATE DATABASE bank_db;
USE bank_db;

CREATE TABLE customer (
    cust_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100), 
    address VARCHAR(200),
    phone VARCHAR(15)
);

CREATE TABLE account (
    acc_no INT AUTO_INCREMENT PRIMARY KEY,
    cust_id INT,
    acc_type VARCHAR(20),
    balance DECIMAL(10,2),
    FOREIGN KEY (cust_id) REFERENCES customer(cust_id)); 
