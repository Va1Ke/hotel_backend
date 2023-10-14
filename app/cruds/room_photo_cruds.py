from fastapi import HTTPException
import databases
from app.schemas import room_photo_schemas
from app.models.models import room_photos
from app.utils.photo import from_base_to_photo, from_photo_to_base, delete_photo
from app.utils.general import ServiceKind


class RoomPhotoCruds:
    def __init__(self, db: databases.Database):
        self.db = db

    async def get_photo_by_kind(self, kind: ServiceKind) -> room_photo_schemas.AddRoomPhoto:
        db_photo = await self.db.fetch_one(room_photos.select().where(room_photos.c.kind == kind.name))
        if db_photo == None:
            return None
        photo_base64 = from_photo_to_base(db_photo.path)
        return room_photo_schemas.AddRoomPhoto(kind=kind, photo=photo_base64)

    async def add_photo(self, room: room_photo_schemas.AddRoomPhoto) -> HTTPException:
        path = from_base_to_photo(room.photo, 'static')
        db_room = room_photos.insert().values(kind=room.kind.name, path=path)
        await self.db.execute(db_room)
        return HTTPException(status_code=200, detail="Success")

    async def change_photo(self, room: room_photo_schemas.AddRoomPhoto) -> HTTPException:
        path = from_base_to_photo(room.photo, 'static')
        old_photo = await self.db.fetch_one(room_photos.select().where(room_photos.c.kind == room.kind.name))
        query = (room_photos.update().where(room_photos.c.kind == room.kind.name).values(
            kind=room.kind.name, path=path
        ).returning(room_photos.c.kind))
        await self.db.execute(query=query)
        delete_photo(old_photo.path)
        return HTTPException(status_code=200, detail="Success")
