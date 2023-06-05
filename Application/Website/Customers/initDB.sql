create database if not exists aegis;
use aegis;

-- DUMP EVERYTHING... YOU REALLY SHOULDN'T DO THIS!
drop table if exists customers;
drop table if exists sessions;
drop table if exists datas;


CREATE TABLE customers (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR (255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE devices (
    ID int primary key AUTO_INCREMENT,
    name varchar(255) not null,
    customerID int,
    FOREIGN KEY (customerID) REFERENCES customers(ID)
)

create table datas (
    ID int primary key AUTO_INCREMENT,
    timestamp timestamp not null default current_timestamp,
    temp float,
    hum float,
    current float,
    senderID int,
    FOREIGN KEY (senderID) REFERENCES devices(ID)
)

create table if not exists sessions (
  session_id varchar(64) primary key,
  session_data json not null,
  created_at timestamp not null default current_timestamp
);
