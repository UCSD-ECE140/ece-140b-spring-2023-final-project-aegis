# Necessary Imports
import uvicorn                                    # Used for running the app directly through Python
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
from fastapi.responses import HTMLResponse        # Used for returning HTML responses (JSON is default)
from fastapi.staticfiles import StaticFiles       # Used for making static resources available to server



app = FastAPI()                                   # Specify the "app" that will run the routing
static_files = StaticFiles(directory='public')    # Specify where the static files are located
app.mount('/public', static_files, name='public') # Mount the static files directory to /public

@app.get('/wattage')
def get_wattage() -> JSONResponse:
    response = "dbmanager.get_wattage()"
    return JSONResponse(status_code=200, content=response.json())
@app.get('/temp')
def get_temp() -> JSONResponse:
    response = "dbmanager.get_temp()"
    return JSONResponse(status_code=200, content=response.json())

@app.get('/shutoff/{dongleID}')
def get_display(dongleID: int) -> JSONResponse:
    print("Shutting off dongle: "+str(dongleID))
    return JSONResponse(status_code=200, content = {"status":"success"})

@app.get('/turnon/{dongleID}')
def get_display(dongleID: int) -> JSONResponse:
    print("Turning on dongle: "+str(dongleID))
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
    uvicorn.run("webServer:app", host="127.0.0.1", port=8007, reload=True)