import bluetooth

# Replace 'XX:XX:XX:XX:XX:XX' with the MAC address of your ESP32 device.
bt_addr = "B8:D6:1A:0E:54:82"
port = 1  # Replace with the desired port number.

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((bt_addr, port))

outputBuffer = []
inputBuffer = []

try:
    while True:
        # Read data from the Bluetooth device.
        data = sock.recv(1024)
        print("Received:", data)
        message = input("Enter message to send: ")

        if(message[-1] != '\n'):
            message = message + '\n'
        print("Sending: ", message)
        sock.send(message.encode('utf-8'))

finally:
    sock.close()



# Necessary Imports
import uvicorn                                    # Used for running the app directly through Python
from fastapi import FastAPI, Request, Response
from starlette.responses import JSONResponse
from fastapi.responses import HTMLResponse        # Used for returning HTML responses (JSON is default)

from fastapi.staticfiles import StaticFiles       # Used for making static resources available to server
import numpy as np


app = FastAPI()                                   # Specify the "app" that will run the routing
static_files = StaticFiles(directory='public')    # Specify where the static files are located
app.mount('/public', static_files, name='public') # Mount the static files directory to /public
@app.get('/recieve')
def get_temp() -> JSONResponse:
    data = sock.recv(1024)

    return JSONResponse(status_code=200, content={"data":data.decode('utf-8')})

@app.post('/send/{message}')
def get_display(message: str) -> JSONResponse:
    print(message)
    sock.send(message.encode('utf-8'))
    return JSONResponse(status_code=200, content = {"status":"success"})

@app.get('/', response_class=HTMLResponse)
def get_home(request: Request) -> HTMLResponse:
    """
    Get the homepage
    :param request: the request object
    :return: the homepage
    """
    with open('homepage.html') as html:
        return HTMLResponse(content=html.read(), status_code=200)

# If running the server directly from Python as a module
if __name__ == "__main__":
    uvicorn.run("communicationbz:app", host="127.0.0.1", port=8007, reload=True)
