from fastapi import HTTPException
import databases
from app.schemas import user_room_schemas, room_schemas
from app.models.models import user_rooms
from app.cruds.room_cruds import RoomCruds
from app.cruds.user_cruds import UserCruds
from app.cruds.room_cruds import RoomCruds
import datetime
from sqlalchemy import and_


class UserRoomCruds:
    def __init__(self, db: databases.Database):
        self.db = db

    async def rent_room(self, rent: user_room_schemas.RentRoom) -> HTTPException:
        check = await self.db.fetch_one(
            user_rooms.select().where(
                and_(user_rooms.c.user_email == rent.user_email, user_rooms.c.room_number == rent.room_number)))
        if check:
            raise HTTPException(status_code=400, detail="This room or user already rented")
        db_user = user_rooms.insert().values(user_email=rent.user_email, room_number=rent.room_number,
                                             rented_at=datetime.datetime.now())
        await self.db.execute(db_user)
        return HTTPException(status_code=200, detail="Success")

    async def leave_room(self, email: str) -> HTTPException:
        query = user_rooms.delete().where(user_rooms.c.user_email == email)
        await self.db.execute(query=query)
        return HTTPException(status_code=200, detail="Success")

    async def get_room_by_user(self, email: str) -> room_schemas.RoomCreate:
        response = await self.db.fetch_one(user_rooms.select().where(user_rooms.c.email == email))
        if response == None:
            return None
        room = await RoomCruds(db=self.db).get_room_by_number(response.room_number)
        return room_schemas.RoomCreate(room_number=room.room_number, kind=room.kind, number_of_beds=room.number_of_beds,
                                       price_per_night=room.price_per_night)
