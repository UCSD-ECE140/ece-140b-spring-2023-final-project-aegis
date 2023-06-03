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
db_config = {
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
def create_user(dongleID: str, email:str, first_name:str, last_name: str, username:str, password:str) -> int:
  password_encrypted = Security.encrypt(password)
  db = mysql.connect(**db_config)
  cursor = db.cursor()
  query = "insert into customers (dongleID, email, first_name, last_name, username, password) values (%s, %s, %s, %s, %s, %s)"
  values = (dongleID, email, first_name, last_name, username, password_encrypted)
  cursor.execute(query, values)
  db.commit()
  db.close()
  return cursor.lastrowid

# SELECT SQL query
def select_users(user_id:int=None) -> list:
  db = mysql.connect(**db_config)
  cursor = db.cursor()
  if user_id == None:
    query = f"select ID, dongleID, email, username, password from customers;"
    cursor.execute(query)
    result = cursor.fetchall()
  else:
    query = f"select dongleID, email, first_name, last_name, username, password from customers where ID={user_id};"
    cursor.execute(query)
    result = cursor.fetchone()
  db.close()
  return result

# UPDATE SQL query
def update_user(dongleID:str, email:str, first_name: str, last_name: str, username:str, password:str) -> bool:
  password_encrypted = Security.encrypt(password)
  db = mysql.connect(**db_config)
  cursor = db.cursor()
  print(dongleID)
  query = "update customers set email = %s, first_name=%s, last_name=%s, username=%s, password=%s where dongleID=%s;"
  values = (email, first_name, last_name, username, password, dongleID)
  cursor.execute(query, values)
  db.commit()
  db.close()
  return True if cursor.rowcount == 1 else False

# DELETE SQL query
def delete_user(user_id:int) -> bool:
  db = mysql.connect(**db_config)
  cursor = db.cursor()
  cursor.execute(f"delete from customers where ID={user_id};")
  db.commit()
  db.close()
  return True if cursor.rowcount == 1 else False

# SELECT query to verify hashed password of users
def check_user_password(identifier:str, password:str) -> bool:
  db = mysql.connect(**db_config)
  cursor = db.cursor()
  query = 'select password from customers where username=%s'
  cursor.execute(query, (identifier,))
  result = cursor.fetchone()
  query = 'select password from customers where email=%s'
  cursor.execute(query, (identifier,))
  result1 = cursor.fetchone()
  query = 'select password from customers where dongleID=%s'
  cursor.execute(query, (identifier,))
  result2 = cursor.fetchone()

  if result is not None:
    query = 'select username from customers where password = %s'
    password_decrypted = Security.decrypt(result[0])
    if(password_decrypted == password):
      return True
    else:
       return False
  elif result1 is not None:
    query = 'select username from customers where password = %s'
    password_decrypted = Security.decrypt(result[1])
    if(password_decrypted == password):
      return True
    else:
       return False
  elif result2 is not None:
    query = 'select username from customers where password = %s'
    password_decrypted = Security.decrypt(result[2])
    if(password_decrypted == password):
      return True
    else:
       return False
  return False

## CHANGE TO CHECK DONGLE ID
def verify_availability(dongle_id: str, username: str, email: str) -> str:
    db = mysql.connect(**db_config)
    cursor = db.cursor()

    query = "select id from customers where email = %s"
    cursor.execute(query, (email,))
    result1 = cursor.fetchone()

    query = "select id from customers where username = %s"
    cursor.execute(query, (username,))
    result2 = cursor.fetchone()

    query = "select id from customers where dongleID = %s"
    cursor.execute(query, (dongle_id,))
    result3 = cursor.fetchone()
    cursor.close()
    db.close()
    if result1 and result2 and result3:
        return "all"
    elif result1:
        return "email"
    elif result2:
        return "username"
    elif result3:
        return "dongleID"
    else:
        return "verified"

def find_username(identifier:str) -> str:
  db = mysql.connect(**db_config)
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
      query = 'select username from customers where dongleID = %s;'
      cursor.execute(query, (identifier,))
      result1 = cursor.fetchone()
      cursor.close()
      db.close()
      if result1 is not None:
         return result1[0]
      else:
         return "There is no username associated with this product ID"

def find_password(identifier: str) -> str:
    db = mysql.connect(**db_config)
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
        query = 'select password from customers where dongleID = %s;'
        cursor.execute(query, (identifier,))
        dongleID_result = cursor.fetchone()
        if dongleID_result is not None:
            return Security.decrypt(dongleID_result[0])
        query = 'select password from customers where username = %s;'
        cursor.execute(query, (identifier,))
        username_result = cursor.fetchone()
        cursor.close()
        db.close()
        if username_result is not None:
          return Security.decrypt(username_result[0])
        elif dongleID_result is None and username_result is None:
          return "There is no password associated with this product ID or username"

def get_id(identifier:str) -> str:
  db = mysql.connect(**db_config)
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

      query1 = 'select id from customers where dongleID = %s;'
      cursor.execute(query1, (identifier,))
      dongleID_result = cursor.fetchone()
      cursor.close()
      db.close()
      if username_result is not None:
         return username_result
      elif dongleID_result is not None:
         return dongleID_result
  return "There is no ID associated with this login!"

