from fastapi import HTTPException
import databases
from sqlalchemy import and_
from app.schemas import room_schemas
from app.models.models import rooms


class RoomCruds:
    def __init__(self, db: databases.Database):
        self.db = db

    async def get_room_by_id(self, id: int) -> room_schemas.RoomReturn:
        room = await self.db.fetch_one(rooms.select().where(rooms.c.room_id == id))
        if room == None:
            return None
        return room_schemas.RoomReturn(room_id=room.room_id, kind=room.kind, number_of_beds=room.number_of_beds,
                                       price_per_night=room.price_per_night)

    async def get_free_room_by_number_of_beds(self, number: int) -> list[room_schemas.RoomReturn]:
        db_rooms = await self.db.fetch_all(rooms.select().where(rooms.c.number_of_beds >= number))
        if db_rooms == None:
            return None
        return [room_schemas.RoomReturn(room_id=room.room_id, kind=room.kind, number_of_beds=room.number_of_beds,
                                        price_per_night=room.price_per_night) for room in db_rooms]

    async def create_room(self, room: room_schemas.RoomCreate) -> HTTPException:
        db_room = rooms.insert().values(kind=room.kind.name, number_of_beds=room.number_of_beds,
                                        price_per_night=room.price_per_night)
        await self.db.execute(db_room)
        return HTTPException(status_code=200, detail="Success")

    async def update_room(self, new_room: room_schemas.RoomReturn):
        query = (rooms.update().where(rooms.c.room_id == new_room.room_id).values(
            kind=new_room.kind.name, number_of_beds=new_room.number_of_beds,
            price_per_night=new_room.price_per_night
        ).returning(rooms.c.room_id))
        await self.db.execute(query=query)
        return HTTPException(status_code=200, detail="Contacts successfully updated")

    async def delete_room(self, id: int) -> HTTPException:
        query = rooms.delete().where(rooms.c.room_id == id)
        await self.db.execute(query=query)
        return HTTPException(status_code=200, detail="Success")
