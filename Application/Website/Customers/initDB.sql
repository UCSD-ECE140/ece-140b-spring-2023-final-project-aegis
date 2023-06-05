CREATE DATABASE IF NOT EXISTS aegis CHARACTER SET utf8 COLLATE utf8_bin;
USE aegis;

-- DUMP EVERYTHING... YOU REALLY SHOULDN’T DO THIS!
ALTER TABLE devices
DROP FOREIGN KEY devices_ibfk_1;

ALTER TABLE datas
DROP FOREIGN KEY datas_ibfk_1;

DROP TABLE IF EXISTS devices;
DROP TABLE IF EXISTS datas;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS sessions;

CREATE TABLE customers (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR (255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE sessions (
  session_id varchar(64) primary key,
  session_data json not null,
  created_at timestamp not null default current_timestamp
);

CREATE TABLE devices (
    ID int primary key AUTO_INCREMENT,
    device_id varchar(255) not null,
    customerID int,
    FOREIGN KEY (customerID) REFERENCES customers(ID)
);

CREATE TABLE datas (
    ID int primary key AUTO_INCREMENT,
    time_stamp timestamp not null default current_timestamp,
    temp float,
    hum float,
    current float,
    senderID int,
    FOREIGN KEY (senderID) REFERENCES devices(ID)
);
