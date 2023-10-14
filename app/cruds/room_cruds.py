from fastapi import HTTPException
import databases
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

    async def create_room(self, room: room_schemas.RoomCreate) -> HTTPException:
        db_room = rooms.insert().values(kind=room.kind, number_of_beds=room.number_of_beds,
                                        price_per_night=room.price_per_night)
        await self.db.execute(db_room)
        return HTTPException(status_code=200, detail="Success")

    async def update_room(self, new_room: room_schemas.RoomReturn):
        query = (rooms.update().where(rooms.c.room_id == new_room.room_id).values(
            kind=new_room.kind, number_of_beds=new_room.number_of_beds,
            price_per_night=new_room.price_per_night
        ).returning(rooms.c.room_id))
        await self.db.execute(query=query)
        return HTTPException(status_code=200, detail="Contacts successfully updated")

    async def delete_room(self, id: int) -> HTTPException:
        query = rooms.delete().where(rooms.c.room_id == id)
        await self.db.execute(query=query)
        return HTTPException(status_code=200, detail="Success")
