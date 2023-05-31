# Necessary Imports                              
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse        # Used for returning HTML responses (JSON is default)
from fastapi.staticfiles import StaticFiles       # Used for making static resources available to server
from fastapi.templating import Jinja2Templates
from starlette.responses import JSONResponse
from utilities.sessions import Sessions
from utilities.Models import User, VisitorLogin, VisitorRegister, RetrieveUser, RetrievePass
from utilities.Security import Security
import Customers.customerDB as customerDB
import uvicorn      # Used for running the app directly through Python

app = FastAPI()                                   # Specify the "app" that will run the routing
static_files = StaticFiles(directory='public')    # Specify where the static files are located
views = Jinja2Templates(directory="public/views")
app.mount('/public', static_files, name='public') # Mount the static files directory to /public
sessions = Sessions(secret_key=customerDB.session_config['session_key'], expiry=900)
  
## Route for Website Login
@app.get('/login')
def get_login(request:Request) -> HTMLResponse:
    return HTMLResponse(content=views.get_template("login.html").render(), status_code=200)

## Route for Website Register
@app.get('/register')
def get_login(request:Request) -> HTMLResponse:
    return HTMLResponse(content=views.get_template("register.html").render(), status_code=200)

## Route for QR code
@app.get('/register/{encrypted_dongleID}')
def get_login(request: Request, encrypted_dongleID: str) -> HTMLResponse:
    dongleID = Security.decrypt_dongleID(encrypted_dongleID)
    ## Look in the database for table dongleID
    return HTMLResponse(content=views.get_template("register.html").render(), status_code=200)

## Route for forgetting user
@app.get('/forgot-user')
def retrieve_user(request:Request) -> HTMLResponse:
     return HTMLResponse(content=views.get_template("forgot-user.html").render(), status_code=200)
  
@app.get('/forgot-pass')
def retrieve_user(request:Request) -> HTMLResponse:
     return HTMLResponse(content=views.get_template("forgot-pass.html").render(), status_code=200)

@app.post('/login')
def post_login(visitor:VisitorLogin, request:Request, response:Response) -> dict:
  username = visitor.username
  password = visitor.password

  session = sessions.get_session(request)
  if len(session) > 0:
    sessions.end_session(request, response)

  # Authenticate the user
  if authenticate_user(username, password):
    session_data = {'username': username, 'logged_in': True}
    session_id = sessions.create_session(response, session_data)
    return {'message': 'Login successful', 'session_id': session_id}
  else:
    return {'message': 'Invalid username or password', 'session_id': 0}
  
@app.post('/register')
def post_login(visitor:VisitorRegister, request:Request, response:Response) -> dict:
  dongleID = visitor.dongleID
  username = visitor.username
  password = visitor.password
  return None
  

















## GET ANALYTICS  
## Change to send data of analytics by first transforming it on server
@app.get('/analytics')
def get_wattage() -> JSONResponse:
    response = "dbmanager.get_wattage()"
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
    return HTMLResponse(content=views.get_template("homepage.html").render(), status_code=200)

def authenticate_user(username:str, password:str) -> bool:
  return db.check_user_password(username, password)

# If running the server directly from Python as a module
if __name__ == "__main__":
    uvicorn.run("webServer:app", host="127.0.0.1", port=8007, reload=True)
