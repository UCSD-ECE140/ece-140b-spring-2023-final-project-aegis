# Necessary Imports                              
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse        # Used for returning HTML responses (JSON is default)
from fastapi.staticfiles import StaticFiles       # Used for making static resources available to server
from fastapi.templating import Jinja2Templates
from starlette.responses import JSONResponse
from utilities.sessions import Sessions
from utilities.Models import User, VisitorLogin, VisitorRegister, RetrieveInfo
from utilities.Security import Security
import Customers.Auth as Auth
import uvicorn      # Used for running the app directly through Python
import utilities
app = FastAPI()                                   # Specify the "app" that will run the routing
static_files = StaticFiles(directory='public')    # Specify where the static files are located
views = Jinja2Templates(directory="public/views")
app.mount('/public', static_files, name='public') # Mount the static files directory to /public
sessions = Sessions(secret_key=Auth.session_config['session_key'], expiry=900)
  
## Route for Website Login
@app.get('/login')
def get_login(request:Request) -> HTMLResponse:
    return HTMLResponse(content=views.get_template("login.html").render(), status_code=200)

## Route for Website Register
## Can manually put in product ID through website
@app.get('/register')
def get_login(request:Request) -> HTMLResponse:
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
  

## Check to see if the product dongle exists in our database of users, if so, we return
@app.post('/register/{encrypted_dongleID}')
def post_login(encrypted_dongleID: str, request:Request, response:Response) -> dict:
    dongleID = Security.decrypt_dongleID(encrypted_dongleID)
    ## authenticate dongleID by looking it up in the database of products
    ## Customer database could have product ID but null username, password, and email
    ## If exists, then we return the decrypted dongl
    return None
  
## Route for QR code
@app.get('/register/{encrypted_dongleID}')
def get_login(request: Request, encrypted_dongleID: str) -> HTMLResponse:
    dongleID = Security.decrypt_dongleID(encrypted_dongleID)
    ## Look in the database for table dongleID
    return HTMLResponse(content=views.get_template("register.html").render(), status_code=200)

# RESTful User Routes
# GET /users
@app.get('/users')
def get_users() -> dict:
  users = Auth.select_users()
  keys = ['id', 'dongleID', 'email', 'username']
  users = [dict(zip(keys, user)) for user in users]
  return {"users": users}

# GET /users/{user_id}
@app.get('/users/{user_id}')
def get_user(user_id:int) -> dict:
  user = Auth.select_users(user_id)
  if user:
    return {'id':user[0], 'dongleID':user[1], 'email':user[2], 'username':user[3]}
  return {}

# POST /users
# Used to create a new user
@app.post("/users")
def post_user(user:User) -> dict:
  new_id = Auth.create_user(user.dongleID, user.email, user.username, user.password)
  return get_user(new_id)

# PUT /users/{user_id}
@app.put('/users/{user_id}')
def put_user(user_id:int, user:User) -> dict:
  return {'success': Auth.update_user(user_id, user.dongleID, user.email, user.username, user.password)}

# DELETE /users/{user_id}
@app.delete('/users/{user_id}')
def delete_user(user_id:int) -> dict:
  return {'success': Auth.delete_user(user_id)}

## Registration
@app.post("/check_email_user")
def check_email_exists(user: User) -> str:
  return Auth.verify_availability(user.username, user.email)

## Forgetting Username / Password
## ADD IN COMMENTS
@app.post("/get_user")
def get_username(user: RetrieveInfo) -> str:
  return Auth.find_username(user.identifier)

@app.post("/get_pass")
def get_password(user: RetrieveInfo) -> str:
  return Auth.find_password(user.identifier)















## GET ANALYTICS  
## Change to send data of analytics by first transforming it on server
@app.get('/analytics')
def get_analytics() -> HTMLResponse:
    return HTMLResponse(content=views.get_template("analytics.html").render(), status_code=200)
    #response = "dbmanager.get_wattage()"
    #return JSONResponse(status_code=200, content=response.json())

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


## Helper Functions
## Need to check if user database has username or email
## identifier can be username or email
def authenticate_user(identifier:str, password:str) -> bool:
  return Auth.check_user_password(identifier, password)

# If running the server directly from Python as a module
if __name__ == "__main__":
    uvicorn.run("webServer:app", host="127.0.0.1", port=8007, reload=True)
