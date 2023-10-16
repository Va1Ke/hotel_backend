from pydantic import BaseModel



class UserCreate(BaseModel):
    name: str
    password: str
    email: str


class UserReturn(BaseModel):
    user_id: int
    name: str
    password: str
    email: str
    admin: bool
