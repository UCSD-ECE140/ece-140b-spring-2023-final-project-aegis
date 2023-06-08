import os                   
import random                    # Used for interacting with the system environment
from dotenv import load_dotenv                    # Used to read the credentials
import paho.mqtt.client as mqtt
load_dotenv('credentials.env')                 # Read in the environment variables for MySQL

datas_config = {
  "host": os.environ['MYSQL_HOST'],
  "user": os.environ['MYSQL_USER'],
  "password": os.environ['MYSQL_PASSWORD'],
  "database": os.environ['MYSQL_DATABASE']
}

MQTT_config = {
  "server": os.environ['MQTT_SERVER'],
  "username": os.environ['MQTT_USERNAME'],
  "password": os.environ['MQTT_PASSWORD'],
  "domain": os.environ['MQTT_DOMAIN'],
  "port": os.environ['MQTT_PORT'],
  "topic": os.environ['MQTT_TOPIC']
}

class MQTTServer:
    def __init__(self):
        self.client = mqtt.Client(client_id = MQTT_config['server'], clean_session=True)
        self.client.username_pw_set(username = MQTT_config['username'], password = MQTT_config['password'])
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def start(self):
        self.client.connect(MQTT_config['domain'], int(MQTT_config['port']))
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe(MQTT_config['topic'] + "/#")
        client.publish("Aegis/aegisDongleSend/78:23:38:2F:12:09", "bedroom,25.3,68.0,1.3;")
        client.publish("Aegis/aegisDongleSend/BC:23:68:DF:B2:09", "living room,26.7,68.0,0.9;")
        client.publish("Aegis/aegisDongleSend/FE:23:18:5F:1A:09", "kitchen,27.8,68.0,3.4;")
        client.publish("Aegis/aegisDongleSend/45:23:C2:8F:15:09", "family room,23.4,68.0,0.5;")
        client.publish("Aegis/aegisDongleSend/23:23:C4:FF:12:09", "gaming den,29.3,68.0,15.2;")
        client.publish("Aegis/ecoData", str(random.randint(1000,1250)))
        client.publish("Aegis/ecoData", str(random.randint(1000,1250)))
        client.publish("Aegis/ecoData", str(random.randint(1000,1250)))
        client.publish("Aegis/ecoData", str(random.randint(1000,1250)))
        client.publish("Aegis/ecoData", str(random.randint(1000,1250)))
        client.publish("Aegis/ecoData", str(random.randint(1000,1250)))


    def on_message(self, client, userdata, msg):
        split = msg.topic.split("/")
        if split[0] == "Aegis":
            if split[1] == "aegisDongleSend":
                print(split[1] + " " + msg.payload.decode())
           

# If running the server directly from Python as a module
if __name__ == "__main__":
    mqtt_server = MQTTServer()  
    mqtt_server.start()
