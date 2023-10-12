from pydantic import BaseModel
import datetime

class UserCreate(BaseModel):
    name: str
    password: str
    email: str

class UserReturn(BaseModel):
    user_id: int
    name: str
    password: str
    email: str


