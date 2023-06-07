from pydantic import BaseModel 

## General definition
class User(BaseModel):
  first_name: str
  last_name: str
  email: str
  username: str
  password: str

class UserUpdate(BaseModel):
  first_name: str
  last_name: str
  id: str
  email: str
  username: str
  password: str

class VisitorLogin(BaseModel):
  username: str
  password: str

class RetrieveInfo(BaseModel):
  identifier: str

class Configurations(BaseModel):
  name: str
  temperature_threshold: str
  dongleID: str


