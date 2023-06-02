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

class RetrieveInfo(BaseModel):
  identifier: str

