import bluetooth

# Replace 'XX:XX:XX:XX:XX:XX' with the MAC address of your ESP32 device.
bt_addr = "70:B8:F6:5B:61:BA"
port = 1  # Replace with the desired port number.

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)



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
@app.on_event("startup")
async def startup_event():
    global sock
    sock.connect((bt_addr, port))

@app.get('/recieve')
def get_temp() -> JSONResponse:
    data = sock.recv(1024)

    return JSONResponse(status_code=200, content={"data":data.decode('utf-8')})

@app.get('/on')
def get_display() -> JSONResponse:
    message = "on"
    sock.send(message.encode('utf-8'))
    return JSONResponse(status_code=200, content = {"status":"success"})

@app.get('/off')
def get_display() -> JSONResponse:
    message = "off"
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
    uvicorn.run("communicationbz:app", host="127.0.0.1", port=8009, reload=True)
