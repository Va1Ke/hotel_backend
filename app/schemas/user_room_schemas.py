from pydantic import BaseModel


class RentRoom(BaseModel):
    user_email: str
    room_number: int
