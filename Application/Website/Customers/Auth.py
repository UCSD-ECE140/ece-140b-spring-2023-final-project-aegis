''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Necessary Imports
import mysql.connector as mysql                   # Used for interacting with the MySQL database
import os                                         # Used for interacting with the system environment
from dotenv import load_dotenv                    # Used to read the credentials
import sys
sys.path.append('../')
from utilities.Security import Security
import bcrypt

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
## COPY PASTED FROM 140A AND MODIFIED
# Configuration
load_dotenv('credentials.env')                 # Read in the environment variables for MySQL
config = {
  "host": os.environ['MYSQL_HOST'],
  "user": os.environ['MYSQL_USER'],
  "password": os.environ['MYSQL_PASSWORD'],
  "database": os.environ['MYSQL_DATABASE']
}
session_config = {
  'session_key': os.environ['SESSION_KEY']
}

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Define helper functions for CRUD operations
# Create unique user.
def create_user(first_name:str, last_name: str, email: str, username:str, password:str) -> int:
  password_encrypted = Security.encrypt(password)
  db = mysql.connect(**config)
  cursor = db.cursor()
  query = "insert into customers (email, first_name, last_name, username, password) values (%s, %s, %s, %s, %s)"
  values = (email, first_name, last_name, username, password_encrypted)
  cursor.execute(query, values)
  db.commit()
  db.close()
  return cursor.lastrowid

# SELECT SQL query
def select_users(user_id:int=None) -> list:
  db = mysql.connect(**config)
  cursor = db.cursor()
  if user_id == None:
    query = f"select ID, email, first_name, last_name, username, password from customers;"
    cursor.execute(query)
    result = cursor.fetchall()
  else:
    query = f"select ID, email, first_name, last_name, username, password from customers where ID={user_id};"
    cursor.execute(query)
    result = cursor.fetchone()
  db.close()
  return result

# UPDATE SQL query
def update_user(ID:str, first_name: str, last_name: str, email: str, username:str, password:str) -> bool:
  db = mysql.connect(**config)
  cursor = db.cursor()
  query = "update customers set email = %s, first_name=%s, last_name=%s, username=%s, password=%s where ID=%s;"
  values = (email, first_name, last_name, username, password, ID)
  cursor.execute(query, values)
  db.commit()
  db.close()
  return True if cursor.rowcount == 1 else False

# DELETE SQL query
def delete_user(user_id:int) -> bool:
  db = mysql.connect(**config)
  cursor = db.cursor()
  cursor.execute(f"delete from customers where ID={user_id};")
  db.commit()
  db.close()
  return True if cursor.rowcount == 1 else False

# SELECT query to verify hashed password of users
def check_user_password(identifier:str, password:str) -> bool:
  db = mysql.connect(**config)
  cursor = db.cursor()
  query = 'select password from customers where username=%s'
  cursor.execute(query, (identifier,))
  result = cursor.fetchone()
  query = 'select password from customers where email=%s'
  cursor.execute(query, (identifier,))
  result1 = cursor.fetchone()
  if result is not None:
    query = 'select username from customers where password = %s'
    password_decrypted = Security.decrypt(result[0])
    if(password_decrypted == password):
      return True
    else:
       return False
  elif result1 is not None:
    query = 'select username from customers where password = %s'
    password_decrypted = Security.decrypt(result1[0])
    if(password_decrypted == password):
      return True
    else:
       return False
  return False

## CHANGE TO CHECK DONGLE ID
def verify_availability(username: str, email: str) -> str:
    db = mysql.connect(**config)
    cursor = db.cursor()

    query = "select id from customers where email = %s"
    cursor.execute(query, (email,))
    result1 = cursor.fetchone()

    query = "select id from customers where username = %s"
    cursor.execute(query, (username,))
    result2 = cursor.fetchone()

    cursor.close()
    db.close()
    if result1 and result2:
        return "all"
    elif result1:
        return "email"
    elif result2:
        return "username"
    else:
        return "verified"

def find_username(identifier:str) -> str:
  db = mysql.connect(**config)
  cursor = db.cursor()
  if('@' in identifier):
      query = 'select username from customers where email = %s;'
      cursor.execute(query, (identifier,))
      result = cursor.fetchone()
      cursor.close()
      db.close()
      if result is not None:
         return result[0]
      else:
         return "There is no username associated with this email"
  else:
     return "Not a valid email"

def find_password(identifier: str) -> str:
    db = mysql.connect(**config)
    cursor = db.cursor()
    if '@' in identifier:
        query = 'select password from customers where email = %s;'
        cursor.execute(query, (identifier,))
        email_result = cursor.fetchone()
        cursor.close()
        db.close()
        if email_result is not None:
            return Security.decrypt(email_result[0])
        else:
            return "There is no password associated with this email"
    else:
        query = 'select password from customers where username = %s;'
        cursor.execute(query, (identifier,))
        username_result = cursor.fetchone()
        cursor.close()
        db.close()
        if username_result is not None:
          return Security.decrypt(username_result[0])
        elif username_result is None:
          return "There is no password associated with this username"

def get_id(identifier:str) -> str:
  db = mysql.connect(**config)
  cursor = db.cursor()
  if('@' in identifier):
      query = 'select id from customers where email = %s;'
      cursor.execute(query, (identifier,))
      email_result = cursor.fetchone()
      cursor.close()
      db.close()
      if email_result is not None:
         return email_result
  else:
      query = 'select id from customers where username = %s;'
      cursor.execute(query, (identifier,))
      username_result = cursor.fetchone()
      cursor.close()
      db.close()
      if username_result is not None:
         return username_result[0]
  return "There is no ID associated with this login!"

def add_device(device_id: str, ID: str) -> str:
   db = mysql.connect(**config)
   cursor = db.cursor()
   query = 'INSERT INTO customers_devices (device_id, customerID) values (%s, %s)' 
   values = (device_id, ID)
   cursor.execute(query, values)
   results = cursor.fetchone()
   db.commit()
   db.close()
   return cursor.lastrowid

def delete_device(device_id: str) -> bool:
   db = mysql.connect(**config)
   cursor = db.cursor()
   query = 'delete from customers_devices where devices_id = %s' 
   values = (device_id, device_id)
   cursor.execute(query, values)
   results = cursor.fetchone()
   db.commit()
   db.close()
   return True if cursor.rowcount == 1 else False

def get_device(device_ID: str) -> bool:
   db = mysql.connect(**config)
   cursor = db.cursor()
   query = 'SELECT customerID FROM customers_devices WHERE device_id = %s'
   cursor.execute(query, (device_ID,))
   results = cursor.fetchall()
   db.commit()
   db.close()
   return True if cursor.rowcount == 0 else False

def create_user(first_name:str, last_name: str, email: str, username:str, password:str) -> int:
  password_encrypted = Security.encrypt(password)
  db = mysql.connect(**config)
  cursor = db.cursor()
  query = "insert into customers (email, first_name, last_name, username, password) values (%s, %s, %s, %s, %s)"
  values = (email, first_name, last_name, username, password_encrypted)
  cursor.execute(query, values)
  db.commit()
  db.close()
  return cursor.lastrowid

def get_configurations(account_id: str) -> list:
    db = mysql.connect(**config)
    cursor = db.cursor()

    query = """
        SELECT *
        FROM device_permissions
        WHERE device_id = %s;
    """
    cursor.execute(query, (account_id,))
    device_permissions = cursor.fetchall()

    db.close()
    return device_permissions

# UPDATE SQL query
def update_configurations(name: str, temperature_threshold: str, dongleID: str) -> bool:
  db = mysql.connect(**config)
  cursor = db.cursor()
  query = "update device_permissions set name = %s, temperature_threshold=%s where dongleID = %s;"
  values = (name, temperature_threshold, dongleID)
  cursor.execute(query, values)
  result = cursor.fetchone()
  db.close()
  return True if cursor.rowcount == 1 else False

def verify_permissions(device_id: str, dongleID: str) -> bool:
  db = mysql.connect(**config)
  cursor = db.cursor()
  query = "SELECT * FROM device_permissions WHERE device_id = %s AND dongle_id = %s;"
  values = (device_id, dongleID)
  cursor.execute(query, values)
  result = cursor.fetchall()
  db.close()
  return True if cursor.rowcount == 1 else False

def calculate_data(account_id):
    db = mysql.connect(**config)
    cursor = db.cursor()

    query = """
        SELECT d.* 
    FROM datas d
    JOIN device_permissions dp ON d.senderID = dp.dongleID
    JOIN customers_devices cd ON dp.device_id = cd.customerID
    WHERE cd.customerID = %s;
    """
    cursor.execute(query, (account_id,))
    data = cursor.fetchall()
    cursor.close()
    db.close()

    return data