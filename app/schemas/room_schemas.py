from pydantic import BaseModel

from app.utils.general import ServiceKind


class RoomCreate(BaseModel):
    room_number: int
    kind: ServiceKind
    number_of_beds: int
    price_per_night: int


class RoomReturn(BaseModel):
    room_id: int
    room_number: int
    kind: ServiceKind
    number_of_beds: int
    price_per_night: int
