# import bluetooth

# Replace 'XX:XX:XX:XX:XX:XX' with the MAC address of your ESP32 device.
#bt_addr = "70:B8:F6:5B:61:BA"
#port = 1  # Replace with the desired port number.#

#sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

# Necessary Imports
import uvicorn                                    # Used for running the app directly through Python
from fastapi import FastAPI, Request, Response
from starlette.responses import JSONResponse
from fastapi.responses import HTMLResponse        # Used for returning HTML responses (JSON is default)

from fastapi.staticfiles import StaticFiles       # Used for making static resources available to server
import numpy as np
import paho.mqtt.client as mqtt


app = FastAPI()                                   # Specify the "app" that will run the routing
static_files = StaticFiles(directory='public')    # Specify where the static files are located
app.mount('/public', static_files, name='public') # Mount the static files directory to /public
buffer = ""
client = None

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected")
    else:
        print("Connection failed")

def on_message(client, userdata, msg):
    global buffer
    print(f"Message received: {msg.payload.decode()} from Topic: {msg.topic}")
    buffer += msg.payload.decode()



@app.on_event("startup")
async def startup_event():
    global client
    client = mqtt.Client("aegis5eb678699")
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("broker.hivemq.com", 1883)

    client.loop_start()  # Start the loop in a new threadgm
    client.subscribe("aegisDongleSend")

@app.get('/recieve')
def get_temp() -> JSONResponse:
    global client
    global buffer
    client.loop()
    sendTo = buffer
    buffer = ""
    return JSONResponse(status_code=200, content={"data":sendTo})

@app.get('/on')
def get_display() -> JSONResponse:
    global client
    #(rc, mid) = client.publish("aegisDongleReceive", "on", qos=0)
    return JSONResponse(status_code=200, content = {"status":"success"})

@app.get('/off')
def get_display() -> JSONResponse:
    global client
    #(rc, mid) = client.publish("aegisDongleReceive", "off", qos=0)
    return JSONResponse(status_code=200, content = {"status":"success"})

@app.get('/', response_class=HTMLResponse)
def get_home(request: Request) -> HTMLResponse:
    """
    Get the homepage
    :param request: the request object
    :return: the homepageg
    """
    with open('homepage.html') as html:
        return HTMLResponse(content=html.read(), status_code=200)

# If running the server directly from Python as a module
if __name__ == "__main__":
    uvicorn.run("communicationbz:app", host="127.0.0.1", port=8009, reload=True)
