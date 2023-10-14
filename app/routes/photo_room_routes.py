from fastapi import APIRouter, Depends
from fastapi import HTTPException
from app.cruds.room_photo_cruds import RoomPhotoCruds
from app.cruds.user_cruds import UserCruds
from app.cruds.room_cruds import RoomCruds
from app.database import db
from app.schemas.room_photo_schemas import *
from app.utils.jwt import get_login_from_token
from app.utils.general import ServiceKind

router = APIRouter()

@router.post("/photo/", tags=["Photo"])
async def add_photo(new_photo: AddRoomPhoto, email_from_jwt: str = Depends(get_login_from_token)):
    user = await UserCruds(db=db).get_user_by_email(email_from_jwt)
    if user.admin:
        await RoomPhotoCruds(db=db).add_photo(new_photo)
        return {
            "result": "photo added successfully"
        }
    raise HTTPException(status_code=400, detail="No permissions to do this")

@router.get("/photo/", tags=["Photo"])
async def get_photo(room_id: int, email_from_jwt: str = Depends(get_login_from_token)):
    user = await UserCruds(db=db).get_user_by_email(email_from_jwt)
    if user.admin:
        room = await RoomCruds(db=db).get_room_by_id(room_id)
        return await RoomPhotoCruds(db=db).get_photo_by_kind(room.kind)
    raise HTTPException(status_code=400, detail="No permissions to do this")

@router.put("/photo/", tags=["Photo"])
async def update_photo(new_photo: AddRoomPhoto, email_from_jwt: str = Depends(get_login_from_token)):
    user = await UserCruds(db=db).get_user_by_email(email_from_jwt)
    if user.admin:
        await RoomPhotoCruds(db=db).change_photo(new_photo)
        return {
            "result": "photo added successfully"
        }
    raise HTTPException(status_code=400, detail="No permissions to do this")

