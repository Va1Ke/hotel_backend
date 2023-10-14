from fastapi import HTTPException
import databases
from app.schemas import user_schemas
from app.models.models import users


class UserCruds:
    def __init__(self, db: databases.Database):
        self.db = db

    async def get_user_by_id(self, id: int) -> user_schemas.UserReturn:
        user = await self.db.fetch_one(users.select().where(users.c.user_id == id))
        if user == None:
            return None
        return user_schemas.UserReturn(user_id=user.user_id, email=user.email, password=user.password,
                                       name=user.name, admin=user.admin)

    async def get_user_by_email(self, email: str) -> user_schemas.UserReturn:
        user = await self.db.fetch_one(users.select().where(users.c.email == email))
        if user == None:
            return None
        return user_schemas.UserReturn(user_id=user.user_id, email=user.email, password=user.password, name=user.name,
                                       admin=user.admin)

    async def get_users(self, skip: int = 0, limit: int = 100) -> list[user_schemas.UserReturn]:
        query = users.select().offset(skip).limit(limit)
        users_to_dict = await self.db.fetch_all(query=query)
        return [user_schemas.UserReturn(**user) for user in users_to_dict]

    async def create_user(self, user: user_schemas.UserCreate) -> HTTPException:
        db_user = users.insert().values(email=user.email, password=user.password, name=user.name)
        await self.db.execute(db_user)
        return HTTPException(status_code=200, detail="Success")

    async def delete_user(self, email: str) -> HTTPException:
        query = users.delete().where(users.c.email == email)
        await self.db.execute(query=query)
        return HTTPException(status_code=200, detail="Success")
