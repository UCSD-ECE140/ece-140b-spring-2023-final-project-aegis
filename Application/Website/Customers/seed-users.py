''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import mysql.connector as mysql
import os                                         # Used for interacting with the system environment
import sys
sys.path.append('../')
from utilities.Security import Security
from dotenv import load_dotenv                    # Used to read the credentials

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Collection of users with plain-text passwords – BIG NONO! NEVER EVER DO THIS!!!
users = [
  {'email':'admin@admin.ucsd', 'first_name':'Admin', 'last_name':'Admin', 'username':'admin', 'password':'aegis'}
]

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Connect to the database
load_dotenv('../credentials.env')
config = {
  'host': os.environ['MYSQL_HOST'],
  'user': os.environ['MYSQL_USER'],
  'password': os.environ['MYSQL_PASSWORD'],
  'database': os.environ['MYSQL_DATABASE']
}
db = mysql.connect(**config)
cursor = db.cursor()

# Generate a salt for extra security

# Insert every user with a salted and hashed password
for user in users:
  pwd = Security.encrypt(user['password'])
  query = "insert into customers (email, first_name, last_name, username, password) values (%s, %s, %s, %s, %s)"
  values = (user['email'], user['first_name'], user['last_name'], user['username'], pwd)
  cursor.execute(query, values)

# Commit the changes and close the connection
db.commit()
cursor.close()
db.close()

print('Users seeded.')
import mysql.connector
import os
from dotenv import load_dotenv

# Connect to the database
load_dotenv('../credentials.env')
config = {
    'host': os.environ['MYSQL_HOST'],
    'user': os.environ['MYSQL_USER'],
    'password': os.environ['MYSQL_PASSWORD'],
    'database': os.environ['MYSQL_DATABASE']
}
db = mysql.connector.connect(**config)
cursor = db.cursor()

customer_data = [
    ('Michael', 'Scott', 'michaelscott', 'michaelscott@email.com', 'password123'),
    ('Pam', 'Beesly', 'pambeesly', 'pambeesly@email.com', 'password123'),
    ('Jim', 'Halpert', 'jimhalpert', 'jimhalpert@email.com', 'password123'),
    ('Dwight', 'Schrute', 'dwightschrute', 'dwightschrute@email.com', 'password123'),
    ('Angela', 'Martin', 'angelamartin', 'angelamartin@email.com', 'password123'),
    ('Oscar', 'Martinez', 'oscarmartinez', 'oscarmartinez@email.com', 'password123'),
    ('Stanley', 'Hudson', 'stanleyhudson', 'stanleyhudson@email.com', 'password123'),
    ('Phyllis', 'Vance', 'phyllisvance', 'phyllisvance@email.com', 'password123')
]
hashed_customer_data = [(first_name, last_name, username, email, Security.encrypt(password))
                        for first_name, last_name, username, email, password in customer_data]
customer_query = "INSERT INTO customers (first_name, last_name, username, email, password) VALUES (%s, %s, %s, %s, %s)"
cursor.executemany(customer_query, hashed_customer_data)
# Inserting devices for customers
device_data = [
    ('device1', 1),
    ('device2', 2),
    ('device3', 3),
    ('device4', 4),
    ('device5', 5),
    ('device6', 6),
    ('device7', 7),
    ('device8', 8)
]
device_query = "INSERT INTO customers_devices (device_id, customerID) VALUES (%s, %s)"
cursor.executemany(device_query, device_data)

# Inserting device permissions
permission_data = [
    ('Thermostat 1', 22, True, 'dongle1', 'device1'),
    ('Thermostat 2', 23, False, 'dongle2', 'device2'),
    ('Thermostat 3', 21, True, 'dongle3', 'device3'),
    ('Thermostat 4', 20, False, 'dongle4', 'device4'),
    ('Thermostat 5', 24, True, 'dongle5', 'device5'),
    ('Thermostat 6', 22, False, 'dongle6', 'device6'),
    ('Thermostat 7', 23, True, 'dongle7', 'device7'),
    ('Thermostat 8', 24, False, 'dongle8', 'device8')
]
permission_query = "INSERT INTO device_permissions (name, temperature_threshold, state, dongleID, device_id) VALUES (%s, %s, %s, %s, %s)"
cursor.executemany(permission_query, permission_data)

# Inserting datas
data_query = "INSERT INTO datas (time_stamp, temp, hum, current, senderID) VALUES (NOW(), %s, %s, %s, %s)"
data_values = [
    (22, 50, 5, 'dongle1'),
    (23, 55, 6, 'dongle2'),
    (21, 52, 5.5, 'dongle3'),
    (20, 54, 5.2, 'dongle4'),
    (24, 51, 5.3, 'dongle5'),
    (22, 53, 5.7, 'dongle6'),
    (23, 50, 5.1, 'dongle7'),
    (24, 52, 5.8, 'dongle8')
]
cursor.executemany(data_query, data_values)

# Commit the changes and close the connection
db.commit()
cursor.close()
db.close()

print('Demo data inserted successfully.')
