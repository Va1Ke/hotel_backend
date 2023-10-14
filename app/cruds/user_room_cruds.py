from fastapi import HTTPException
import databases
from app.schemas import user_room_schemas
from app.models.models import user_rooms


class UserRoomCruds:
    def __init__(self, db: databases.Database):
        self.db = db

    async def rent_room(self, rent: user_room_schemas.RentRoom) -> HTTPException:
        db_user = user_rooms.insert().values(user_id=rent.user_id, room_id=rent.room_id,
                                             rented_at=rent.rented_at)
        await self.db.execute(db_user)
        return HTTPException(status_code=200, detail="Success")

    async def leave_room(self, user_id: int) -> HTTPException:
        query = user_rooms.delete().where(user_rooms.c.user_id == user_id)
        await self.db.execute(query=query)
        return HTTPException(status_code=200, detail="Success")
