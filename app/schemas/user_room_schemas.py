from pydantic import BaseModel


class RentRoom(BaseModel):
    user_id: int
    room_id: int
