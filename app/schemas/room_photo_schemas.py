from pydantic import BaseModel

from app.utils import ServiceKind


class AddRoomPhoto(BaseModel):
    kind: ServiceKind
    photo: str
