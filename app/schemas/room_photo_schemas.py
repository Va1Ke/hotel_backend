from pydantic import BaseModel

from app.utils.general import ServiceKind


class AddRoomPhoto(BaseModel):
    kind: ServiceKind
    photo: str
