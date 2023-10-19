from fastapi import APIRouter, Depends
from fastapi import HTTPException
from app.cruds.user_room_cruds import UserRoomCruds
from app.cruds.room_cruds import RoomCruds
from app.cruds.user_cruds import UserCruds
from app.database import db
from app.schemas.room_schemas import *
from app.utils.jwt import get_login_from_token

router = APIRouter()


@router.post("/room/add/", tags=["Room"])
async def add_room(new_room: RoomCreate, email_from_jwt: str = Depends(get_login_from_token)):
    user = await UserCruds(db=db).get_user_by_email(email_from_jwt)
    if user.admin:
        await RoomCruds(db=db).create_room(new_room)
        return {
            "result": "room added successfully"
        }
    raise HTTPException(status_code=400, detail="No permissions to do this")


@router.get("/room-by-user/", tags=["Room"])
async def get_room(user_email: str, email_from_jwt: str = Depends(get_login_from_token)):
    user = await UserCruds(db=db).get_user_by_email(email_from_jwt)
    if user.admin:
        return await UserRoomCruds(db=db).get_room_by_user(user_email)
    raise HTTPException(status_code=400, detail="No permissions to do this")


@router.get("/available/room/", tags=["Room"])
async def get_free_room(email_from_jwt: str = Depends(get_login_from_token)):
    user = await UserCruds(db=db).get_user_by_email(email_from_jwt)
    if user.admin:
        return await RoomCruds(db=db).get_available_rooms()
    raise HTTPException(status_code=400, detail="No permissions to do this")


@router.put("/room/update/", tags=["Room"])
async def update_room(new_room: RoomCreate, email_from_jwt: str = Depends(get_login_from_token)):
    user = await UserCruds(db=db).get_user_by_email(email_from_jwt)
    if user.admin:
        await RoomCruds(db=db).update_room(new_room)
        return {
            "result": "room updated successfully"
        }
    raise HTTPException(status_code=400, detail="No permissions to do this")


@router.delete("/room/delete/", tags=["Room"])
async def delete_room(room_number: int, email_from_jwt: str = Depends(get_login_from_token)):
    user = await UserCruds(db=db).get_user_by_email(email_from_jwt)
    if user.admin:
        await RoomCruds(db=db).delete_room(room_number)
        return {
            "result": "room deleted successfully"
        }
    raise HTTPException(status_code=400, detail="No permissions to do this")
