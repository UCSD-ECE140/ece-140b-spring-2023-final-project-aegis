CREATE DATABASE IF NOT EXISTS aegis CHARACTER SET utf8 COLLATE utf8_bin;
USE aegis;

DROP TABLE IF EXISTS datas;
DROP TABLE IF EXISTS schedule;
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

CREATE TABLE customers_devices (
                                   device_id varchar(255) unique,
                                   customerID int,
                                   FOREIGN KEY (customerID) REFERENCES customers(ID)
);

-- Create the 'device_permissions' table
CREATE TABLE device_permissions (
                                    name varchar(255) null,
                                    temperature_threshold int null,
                                    state boolean null,
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

-- Create the 'schedule' table
-- hear the action is the action that needs to be run and the topic is the topic to run it for
CREATE TABLE schedule (
                          ID int primary key AUTO_INCREMENT,
                          device_id varchar(255),
                          time timestamp not null,
                          topic varchar(255) not null,
                          run_action varchar(255) not null,
                          FOREIGN KEY (device_id) REFERENCES customers_devices(device_id)
);

-- Insert demo data into 'customers' table
-- Insert more customers
INSERT INTO customers(first_name, last_name, username, email, password)
VALUES
    ('Michael', 'Scott', 'michaelscott', 'michaelscott@email.com', SHA2('password123', 256)),
    ('Pam', 'Beesly', 'pambeesly', 'pambeesly@email.com', SHA2('password123', 256)),
    ('Jim', 'Halpert', 'jimhalpert', 'jimhalpert@email.com', SHA2('password123', 256)),
    ('Dwight', 'Schrute', 'dwightschrute', 'dwightschrute@email.com', SHA2('password123', 256)),
    ('Angela', 'Martin', 'angelamartin', 'angelamartin@email.com', SHA2('password123', 256)),
    ('Oscar', 'Martinez', 'oscarmartinez', 'oscarmartinez@email.com', SHA2('password123', 256)),
    ('Stanley', 'Hudson', 'stanleyhudson', 'stanleyhudson@email.com', SHA2('password123', 256)),
    ('Phyllis', 'Vance', 'phyllisvance', 'phyllisvance@email.com', SHA2('password123', 256));


-- Inserting devices for customers
INSERT INTO customers_devices(device_id, customerID)
VALUES
    ('device1', 1),
    ('device2', 2),
    ('device3', 3),
    ('device4', 4),
    ('device5', 5),
    ('device6', 6),
    ('device7', 7),
    ('device8', 8);

-- Inserting device permissions
INSERT INTO device_permissions(name, temperature_threshold, state, dongleID, device_id)
VALUES
    ('Thermostat 1', 22, true, 'dongle1', 'device1'),
    ('Thermostat 2', 23, false, 'dongle2', 'device2'),
    ('Thermostat 3', 21, true, 'dongle3', 'device3'),
    ('Thermostat 4', 20, false, 'dongle4', 'device4'),
    ('Thermostat 5', 24, true, 'dongle5', 'device5'),
    ('Thermostat 6', 22, false, 'dongle6', 'device6'),
    ('Thermostat 7', 23, true, 'dongle7', 'device7'),
    ('Thermostat 8', 24, false, 'dongle8', 'device8');

-- Inserting datas
INSERT INTO datas(time_stamp, temp, hum, current, senderID)
VALUES
    (NOW(), 22, 50, 5, 'dongle1'),
    (NOW(), 23, 55, 6, 'dongle2'),
    (NOW(), 21, 52, 5.5, 'dongle3'),
    (NOW(), 20, 54, 5.2, 'dongle4'),
    (NOW(), 24, 51, 5.3, 'dongle5'),
    (NOW(), 22, 53, 5.7, 'dongle6'),
    (NOW(), 23, 50, 5.1, 'dongle7'),
    (NOW(), 24, 52, 5.8, 'dongle8');

-- Inserting into schedule
INSERT INTO schedule(device_id, time, topic, run_action)
VALUES
    ('device1', NOW(), 'aegisDongleReceive', 'off'),
    ('device2', NOW(), 'aegisDongleReceive', 'on'),
    ('device3', NOW(), 'aegisDongleReceive', 'off'),
    ('device4', NOW(), 'aegisDongleReceive', 'on'),
    ('device5', NOW(), 'aegisDongleReceive', 'on'),
    ('device6', NOW(), 'aegisDongleReceive', 'off'),
    ('device7', NOW(), 'aegisDongleReceive', 'off'),
    ('device8', NOW(), 'aegisDongleReceive', 'on');

