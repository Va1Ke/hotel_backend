from fastapi import APIRouter, Depends
from fastapi import HTTPException
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

@router.put("/room/update/", tags=["Room"])
async def update_room(room_id: int, new_room: RoomCreate, email_from_jwt: str = Depends(get_login_from_token)):
    user = await UserCruds(db=db).get_user_by_email(email_from_jwt)
    if user.admin:
        new_info = RoomReturn(room_id=room_id, kind=new_room.kind, number_of_beds=new_room.number_of_beds,
                              price_per_night=new_room.price_per_night)
        await RoomCruds(db=db).update_room(new_info)
        return {
            "result": "room updated successfully"
        }
    raise HTTPException(status_code=400, detail="No permissions to do this")


@router.delete("/room/delete/", tags=["Room"])
async def delete_room(room_id: int, email_from_jwt: str = Depends(get_login_from_token)):
    user = await UserCruds(db=db).get_user_by_email(email_from_jwt)
    if user.admin:
        await RoomCruds(db=db).delete_room(room_id)
        return {
            "result": "room deleted successfully"
        }
    raise HTTPException(status_code=400, detail="No permissions to do this")
