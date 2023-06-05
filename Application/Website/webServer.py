# Necessary Imports                              
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse        # Used for returning HTML responses (JSON is default)
from fastapi.staticfiles import StaticFiles       # Used for making static resources available to server
from fastapi.templating import Jinja2Templates
from starlette.responses import JSONResponse
from utilities.sessions import Sessions
from utilities.Models import User, UserUpdate, VisitorLogin, RetrieveInfo
from utilities.Security import Security
from utilities.MQTTServer import MQTTServer
import Customers.Auth as Auth
import uvicorn      # Used for running the app directly through Python
import utilities
import uuid

app = FastAPI()                                   # Specify the "app" that will run the routing
static_files = StaticFiles(directory='public')    # Specify where the static files are located
views = Jinja2Templates(directory="public/views")
app.mount('/public', static_files, name='public') # Mount the static files directory to /public
sessions = Sessions(secret_key=Auth.session_config['session_key'], expiry=0)
mqtt_server = MQTTServer()

@app.on_event('startup')
async def startup():
    mqtt_server.start()

@app.on_event('shutdown')
async def shutdown():
    mqtt_server.stop()
  
## Route for Website Register
## Can manually put in product ID through website
@app.get('/', response_class=HTMLResponse)
def get_home(request: Request) -> HTMLResponse:
    """
    Get the homepage
    :param request: the request object
    :return: the homepage
    """
    return HTMLResponse(content=views.get_template("home.html").render(), status_code=200)

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

@app.get('/profile')
def get_profile(request: Request) -> HTMLResponse:
    session = sessions.get_session(request)
    if len(session) > 0 and session.get('logged_in'):
        session_id = request.cookies.get("session_id")
        if('@' in session['username']):
            email = session.get('username')
            account_id = Auth.get_id(email)
        else:
            username = session.get('username')
            account_id = Auth.get_id(username)
        
        data = Auth.select_users(account_id)
        new_session = {'ID': data[0], 'email': data[1], 'first_name': data[2], 'last_name': data[3], 'username': data[4], 'password': Security.decrypt(data[5]), 'logged_in': session['logged_in']}
        template_data = {'request': request, 'session': new_session, 'session_id': session_id}
        return views.TemplateResponse('profile.html', template_data)
  
    return RedirectResponse(url="/", status_code=302)

## GET ANALYTICS  
## Change to send data of analytics by first transforming it on server
@app.get('/analytics')
def get_profile(request:Request) -> HTMLResponse:
 session = sessions.get_session(request)
 if len(session) > 0 and session.get('logged_in'):
    return None #views.TemplateResponse('profile.html', template_data)
 else:
    return RedirectResponse(url="/", status_code=302)

## Route for QR code
@app.get('/register/{encrypted_dongleID}')
def get_login(request: Request, encrypted_dongleID: str) -> HTMLResponse:
    dongleID = Security.decrypt(encrypted_dongleID)
    ## Look in the database for table dongleID
    return HTMLResponse(content=views.get_template("register.html").render(), status_code=200)

# RESTful User Routes
# GET /users
@app.get('/customers')
def get_users() -> dict:
  users = Auth.select_users()
  keys = ['id', 'dongleID', 'email', 'username']
  users = [dict(zip(keys, user)) for user in users]
  return {"users": users}

# GET /users/{user_id}
@app.get('/customers/{dongle_id}')
def get_user(user_id:int) -> dict:
  user = Auth.select_users(user_id)
  if user:
    return {'id':user[0], 'email':user[1], 'username':user[2]}
  return {}

@app.post('/profile/{UUID}')
def post_login(visitor: VisitorLogin, request: Request, response: Response, UUID: str) -> dict:
    username = visitor.username
    password = visitor.password
    # Authenticate the user
    if authenticate_user(username, password):
        session_data = {'username': username, 'logged_in': True}
        session_id = sessions.create_session(response, session_data)
        device_id = request.cookies.get("device_id")
        if Auth.get_device(UUID) and device_id is None:
            device_id = UUID
            response.set_cookie(key="device_id", value=device_id, expires=None, path="/")
            Auth.add_device(device_id, Auth.get_id(username))
        return {'message': 'Login successful', 'session_id': session_id}
    else:
        return {'message': 'Invalid username or password', 'session_id': 0}
  
  
## Registration
@app.post("/check_customer")
def check_email_exists(user: User) -> str:
  return(Auth.verify_availability(user.username, user.email))

## Check to see if the product dongle exists in our database of users, if so, we return (QR CODE)
@app.post('/register/{encrypted_dongleID}')
def post_login(encrypted_dongleID: str, request:Request, response:Response) -> dict:
    dongleID = Security.decrypt(encrypted_dongleID)
    ## authenticate dongleID by looking it up in the database of products
    ## Customer database could have product ID but null username, password, and email
    ## If exists, then we return the decrypted dongl
    return None

# POST /users
# Used to create a new user
@app.post("/create_customer/{UUID}")
def post_user(user:User, request: Request, response: Response, UUID: str) -> dict:
  ID = Auth.create_user(user.first_name, user.last_name, user.email, user.username, user.password)
  device_id = request.cookies.get("device_id")
  if Auth.get_device(UUID) and device_id is None:
     device_id = UUID
     response.set_cookie(key="device_id", value=device_id, expires=None, path="/")
     Auth.add_device(device_id, Auth.get_id(user.username))
  return {'success': ID}

# PUT /customer/{user_id}
@app.put('/customer/{user_id}')
def put_user(user:User, user_id: str, request: Request) -> dict:
  session = sessions.get_session(request)
  session['username'] = user.username
  return {'success': Auth.update_user(user_id, user.first_name, user.last_name, user.email, user.username, Security.encrypt(user.password))}


# DELETE /product/{user_id}
@app.delete('/customer/{user_id}')
def delete_user(user_id:int) -> dict:
  return {'success': Auth.delete_user(user_id)}

## Forgetting Username / Password
## ADD IN COMMENTS
@app.post("/get_user")
def get_username(user: RetrieveInfo) -> str:
  return Auth.find_username(user.identifier)

@app.post("/get_pass")
def get_password(user: RetrieveInfo) -> str:
  return Auth.find_password(user.identifier)

@app.get('/shutoff/{dongleID}')
def get_display(dongleID: int) -> JSONResponse:
    print("Shutting off dongle: "+str(dongleID))
    return JSONResponse(status_code=200, content = {"status":"success"})

@app.get('/turnon/{dongleID}')
def get_display(dongleID: int) -> JSONResponse:
    print("Turning on dongle: "+str(dongleID))
    return JSONResponse(status_code=200, content = {"status":"success"})

@app.post('/logout')
def post_logout(request:Request, response:Response) -> dict:
  sessions.end_session(request, response)
  return {'message': 'Logout successful', 'session_id': 0}
   

## Helper Functions
## Need to check if user database has username or email
## identifier can be username or email
def authenticate_user(identifier:str, password:str) -> bool:
  return Auth.check_user_password(identifier, password)

# If running the server directly from Python as a module
if __name__ == "__main__":
    uvicorn.run("webServer:app", host="127.0.0.1", port=8007, reload=True)
