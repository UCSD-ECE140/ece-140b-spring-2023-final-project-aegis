from pydantic import BaseModel 

## General definition
class User(BaseModel):
  first_name: str
  last_name: str
  dongleID: str
  email: str
  username: str
  password: str

class VisitorLogin(BaseModel):
  username: str
  password: str

class VisitorRegister(BaseModel):
  dongleID: str
  username: str
  password: str

class RetrieveUser(BaseModel):
  dongleID: str
  email: str

## Model for forgetting password
## Can use any of these
class RetrievePass(BaseModel):
  dongleID: str
  email: str
  username: str

