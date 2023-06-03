import mysql.connector as mysql
from dotenv import load_dotenv
import numpy as np
import os
import datetime
import json


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Configuration
load_dotenv('credentials.env')                 # Read in the environment variables for MySQL
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
"""
Function to serialize the datatime objects for json for fastpi
from stackoverflow
"""
def serialize_datetime(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")


def db_get_recent_weather_update() -> dict:
    db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM weather_updates ORDER BY time DESC LIMIT 1200")
    records = cursor.fetchall()
    dictionary ={}
    db.close()
    i = 0

    for record in records:
        d ={}
        d['temp'] = record[0]
        d['hum'] = record[1]
        d['time'] = json.dumps(record[2], default = serialize_datetime)
        d['bright'] = record[3]
        dictionary[i]=d
        i=i+1
    return dictionary

def db_get_weather_updates() -> list:
    db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM weather_updates ORDER BY time DESC LIMIT 1200")
    records = cursor.fetch()
    returnList=np.array()
    db.close()
    for record in records:
        dictionary ={}
        dictionary['temp'] = record[0]
        dictionary['hum'] = record[1]
        dictionary['time'] = json.dumps(record[2], default = serialize_datetime)
        dictionary['bright'] = record[3]
        returnList = np.append(returnList, dictionary)

    return dictionary

