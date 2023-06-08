import mysql.connector as mysql
import os
import sys
sys.path.append('../')
from utilities.Security import Security
from dotenv import load_dotenv

load_dotenv('../credentials.env')
config = {
    'host': os.environ['MYSQL_HOST'],
    'user': os.environ['MYSQL_USER'],
    'password': os.environ['MYSQL_PASSWORD'],
    'database': os.environ['MYSQL_DATABASE']
}

db = mysql.connect(**config)
cursor = db.cursor()

# Insert demo data into 'customers' table
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

# Commit the changes to the customers table
db.commit()

# Retrieve the auto-generated IDs for customers
cursor.execute("SELECT ID FROM customers")
customer_ids = cursor.fetchall()

# Inserting devices for customers
device_data = [
    ('device1', customer_ids[0][0]),
    ('device2', customer_ids[1][0]),
    ('device3', customer_ids[2][0]),
    ('device4', customer_ids[3][0]),
    ('device5', customer_ids[4][0]),
    ('device6', customer_ids[5][0]),
    ('device7', customer_ids[6][0]),
    ('device8', customer_ids[7][0])
]

device_query = "INSERT INTO customers_devices (device_id, customerID) VALUES (%s, %s)"
cursor.executemany(device_query, device_data)

# Commit the changes to the customers_devices table
db.commit()

# Inserting device permissions
permission_data = [
    ('Living Room Outlet 1', 22, True, 'dongle1', customer_ids[0][0]),
    ('Kitchen Counter Outlet 1', 23, False, 'dongle2', customer_ids[0][0]),
    ('Master Bedroom Outlet 1', 21, True, 'dongle3', customer_ids[0][0]),
    ('Bathroom Outlet 1', 20, False, 'dongle4', customer_ids[0][0]),
    ('Living Room Outlet 2', 24, True, 'dongle5', customer_ids[0][0]),
    ('Bedroom Outlet 1', 22, False, 'dongle6', customer_ids[0][0]),
    ('Bathroom Counter Outlet 2', 23, True, 'dongle7', customer_ids[0][0]),
    ('Bedroom Outlet 2', 24, False, 'dongle8', customer_ids[0][0]),
    ('Living Room Oulet 2', 10, True, 'dongle1_x', customer_ids[1][0]),
    ('Bedroom Outlet 4', 32, False, 'dongle2_x', customer_ids[1][0]),
    ('Master Bedroom Outlet 2', 15, True, 'dongle3_x', customer_ids[1][0]),
    ('Living Room Outlet 3', 32, False, 'dongle4_x', customer_ids[1][0]),
    ('Hallway Outlet 1', 19, True, 'dongle5_x', customer_ids[1][0]),
    ('Master Bedroom Outlet 3', 20, False, 'dongle6_x', customer_ids[1][0]),
    ('Kitchen Counter Outlet 2', 16, True, 'dongle7_x', customer_ids[1][0]),
    ('Hallway Outlet 2', 24, False, 'dongle8_x', customer_ids[1][0])
]

permission_query = "INSERT INTO device_permissions (name, temperature_threshold, state, dongleID, device_id) VALUES (%s, %s, %s, %s, %s)"
cursor.executemany(permission_query, permission_data)

# Commit the changes to the device_permissions table
db.commit()

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
    (24, 52, 5.8, 'dongle8'),
    (22, 50, 5, 'dongle1_x'),
    (23, 55, 6, 'dongle2_x'),
    (21, 52, 5.5, 'dongle3_x'),
    (20, 54, 5.2, 'dongle4_x'),
    (24, 51, 5.3, 'dongle5_x'),
    (22, 53, 5.7, 'dongle6_x'),
    (23, 50, 5.1, 'dongle7_x'),
    (24, 52, 5.8, 'dongle8_x')
]

cursor.executemany(data_query, data_values)

# Commit the changes to the datas table
db.commit()

# Close the cursor and the database connection
cursor.close()
db.close()

print('Demo data inserted successfully.')
