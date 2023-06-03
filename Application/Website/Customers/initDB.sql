create database if not exists aegis;
use aegis;

-- DUMP EVERYTHING... YOU REALLY SHOULDN'T DO THIS!
drop table if exists customers;
drop table if exists sessions;

CREATE TABLE customers (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    dongleID VARCHAR(255) NOT NULL UNIQUE,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR (255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

create table if not exists sessions (
  session_id varchar(64) primary key,
  session_data json not null,
  created_at timestamp not null default current_timestamp
);
