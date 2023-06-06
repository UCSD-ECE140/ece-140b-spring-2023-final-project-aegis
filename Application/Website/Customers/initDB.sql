CREATE DATABASE IF NOT EXISTS aegis CHARACTER SET utf8 COLLATE utf8_bin;
USE aegis;

DROP TABLE IF EXISTS datas;
DROP TABLE IF EXISTS device_permissions;
DROP TABLE IF EXISTS customers_devices;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS sessions;

-- Create the 'customers' table
CREATE TABLE customers (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Create the 'sessions' table
CREATE TABLE sessions (
  session_id varchar(64) primary key,
  session_data json not null,
  created_at timestamp not null default current_timestamp
);

-- Create the 'customers_devices' table
CREATE TABLE customers_devices (
    device_id varchar(255) unique,
    customerID int,
    FOREIGN KEY (customerID) REFERENCES customers(ID)
);

-- Create the 'device_permissions' table
CREATE TABLE device_permissions (
    name varchar(255) null,
    temperature_threshold int null,
    dongleID varchar(255) unique null,
    device_id varchar(255) unique,
    FOREIGN KEY (device_id) REFERENCES customers_devices(device_id)
);

-- Create the 'datas' table
CREATE TABLE datas (
    ID int primary key AUTO_INCREMENT,
    time_stamp timestamp not null default current_timestamp,
    temp float,
    hum float,
    current float,
    senderID varchar(255),
    FOREIGN KEY (senderID) REFERENCES device_permissions(dongleID)
);
