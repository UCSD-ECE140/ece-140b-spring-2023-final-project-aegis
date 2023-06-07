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
