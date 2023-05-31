''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Necessary Imports
import mysql.connector as mysql                   # Used for interacting with the MySQL database
import os                                         # Used for interacting with the system environment
from dotenv import load_dotenv                    # Used to read the credentials
import bcrypt

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
## COPY PASTED FROM 140A, CONFIGURE
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
# CREATE SQL query
def create_user(first_name:str, last_name:str, student_id:int, email:str, username:str, password:str) -> int:
  password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

  db = mysql.connect(**db_config)
  cursor = db.cursor()
  query = "insert into users (first_name, last_name, student_id, email, username, password) values (%s, %s, %s, %s, %s, %s)"
  values = (first_name, last_name, student_id, email, username, password)
  cursor.execute(query, values)
  db.commit()
  db.close()
  return cursor.lastrowid

# SELECT SQL query
def select_users(user_id:int=None) -> list:
  db = mysql.connect(**db_config)
  cursor = db.cursor()
  if user_id == None:
    query = f"select id, first_name, last_name, student_id, email, username from users;"
    cursor.execute(query)
    result = cursor.fetchall()
  else:
    query = f"select id, first_name, last_name, student_id, email, username from users where id={user_id};"
    cursor.execute(query)
    result = cursor.fetchone()
  db.close()
  return result

# UPDATE SQL query
def update_user(user_id:int, first_name:str, last_name:str, student_id:str, email:str, username:str, password:str) -> bool:
  password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
  db = mysql.connect(**db_config)
  cursor = db.cursor()
  query = "update users set first_name=%s, last_name=%s, student_id = %s, email = %s, username=%s, password=%s where id=%s;"
  values = (first_name, last_name, student_id, email, username, password, user_id)
  cursor.execute(query, values)
  db.commit()
  db.close()
  return True if cursor.rowcount == 1 else False

# DELETE SQL query
def delete_user(user_id:int) -> bool:
  db = mysql.connect(**db_config)
  cursor = db.cursor()
  cursor.execute(f"delete from users where id={user_id};")
  db.commit()
  db.close()
  return True if cursor.rowcount == 1 else False

# SELECT query to verify hashed password of users
def check_user_password(username:str, password:str) -> bool:
  db = mysql.connect(**db_config)
  cursor = db.cursor()
  query = 'select password from users where username=%s'
  cursor.execute(query, (username,))
  result = cursor.fetchone()
  query = 'select password from users where email=%s'
  cursor.execute(query, (username,))
  result1 = cursor.fetchone()

  query = 'select username from users where password = %s'
  cursor.execute(query, (password,))
  password_reverse = cursor.fetchone()
  query = 'select email from users where password = %s'
  cursor.execute(query, (password,))
  password_reverse1 = cursor.fetchone()
  cursor.close()
  db.close()

  if password_reverse is not None or password_reverse1 is not None:
     return password_reverse[0] == username or password_reverse1[0] == username 
  if result is not None:
    return bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8'))
  elif result1 is not None:
    return bcrypt.checkpw(password.encode('utf-8'), result1[0].encode('utf-8'))
  return False

def verify_availability(username: str, email: str) -> str:
    db = mysql.connect(**db_config)
    cursor = db.cursor()

    query = "select id from users where email = %s"
    cursor.execute(query, (email,))
    result2 = cursor.fetchone()

    query = "select id from users where username = %s"
    cursor.execute(query, (username,))
    result1 = cursor.fetchone()

    cursor.close()
    db.close()
    if result1 and result2:
        return "both"
    elif result1:
        return "username"
    elif result2:
        return "email"
    else:
        return "verified"

def find_username(email:str) -> str:
  db = mysql.connect(**db_config)
  cursor = db.cursor()
  query = 'select username from users where email=%s'
  cursor.execute(query, (email,))
  result = cursor.fetchone()
  cursor.close()
  db.close()
  if result is not None:
     return result
  return "There is no username associated with this email"

def find_password(email:str) -> str:
  db = mysql.connect(**db_config)
  cursor = db.cursor()
  query = "select password from users where email = %s"
  cursor.execute(query, (email,))
  result2 = cursor.fetchone()

  query = "select password from users where username = %s"
  cursor.execute(query, (email,))
  result1 = cursor.fetchone()
  if result2 is not None:
     result2 = result2[0]
     return result2
  elif result1 is not None:
     result1 = result1[0]
     return result1
  return "There is no password associated with this login"

def get_id(username:str) -> str:
  db = mysql.connect(**db_config)
  cursor = db.cursor()
  if('@' in username):
      query = 'select id from users where email = %s;'
      cursor.execute(query, (username,))
  else:
      query = 'select id from users where username = %s;'
      cursor.execute(query, (username,))
  result = cursor.fetchone()
  cursor.close()
  db.close()
  return result
  
def getData() -> dict:
  db = mysql.connect(**db_config)
  cursor = db.cursor()
  if('@' in username):
    query = 'select id from users where email = %s;'
    cursor.execute(query, (username,))
  else:
    query = 'select id from users where username = %s;'
    cursor.execute(query, (username,))
  result = cursor.fetchone()
  cursor.close()
  db.close()
  return result