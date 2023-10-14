from pydantic import BaseModel

from app.utils.general import ServiceKind


class RoomCreate(BaseModel):
    kind: ServiceKind
    number_of_beds: int
    price_per_night: int


class RoomReturn(BaseModel):
    room_id: int
    kind: ServiceKind
    number_of_beds: int
    price_per_night: int
