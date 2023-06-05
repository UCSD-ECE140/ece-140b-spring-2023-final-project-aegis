import paho.mqtt.client as mqtt

class MQTTServer:
    def __init__(self):
        self.client = mqtt.Client(client_id='AegisServer', clean_session=True)
        self.client.username_pw_set(username="aegisAdmin", password='iLoveAegis!')
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def start(self):
        self.client.connect_async("aegishome.ninja", 8003)
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe("Aegis/#")

    def on_message(self, client, userdata, msg):
        split = msg.topic.split("/")
        if split[0] == "Aegis":
            print(split[1] + " " + msg.payload.decode())


mqtt_server = MQTTServer()