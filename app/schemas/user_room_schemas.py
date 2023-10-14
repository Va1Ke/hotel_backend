from pydantic import BaseModel
import datetime


class RentRoom(BaseModel):
    user_id: int
    room_id: int
    rented_at: datetime.datetime.now()
