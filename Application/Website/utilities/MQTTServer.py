import os                                         # Used for interacting with the system environment
from dotenv import load_dotenv                    # Used to read the credentials
import paho.mqtt.client as mqtt
load_dotenv('credentials.env')                 # Read in the environment variables for MySQL

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
        self.client.connect_async(MQTT_config['domain'], int(MQTT_config['port']))
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe(MQTT_config['topic'] + "/#")

    def on_message(self, client, userdata, msg):
        split = msg.topic.split("/")
        if split[0] == "MQTT_config['topic']":
            print(split[1] + " " + msg.payload.decode())


mqtt_server = MQTTServer()