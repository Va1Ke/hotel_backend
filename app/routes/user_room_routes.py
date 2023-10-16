from fastapi import APIRouter, Depends
from fastapi import HTTPException
from app.cruds.user_cruds import UserCruds
from app.cruds.user_room_cruds import UserRoomCruds
from app.database import db
from app.schemas.user_room_schemas import *
from app.utils.jwt import get_login_from_token

router = APIRouter()


@router.post("/room/rent/", tags=["Manage"])
async def rent_room(user_id: int, room_id: int, email_from_jwt: str = Depends(get_login_from_token)):
    user = await UserCruds(db=db).get_user_by_email(email_from_jwt)
    if user.admin:
        await UserRoomCruds(db=db).rent_room(RentRoom(user_id=user_id, room_id=room_id))
        return {
            "result": "room rented successfully"
        }
    raise HTTPException(status_code=400, detail="No permissions to do this")


@router.post("/room/leave/", tags=["Manage"])
async def leave_room(user_id: int, email_from_jwt: str = Depends(get_login_from_token)):
    user = await UserCruds(db=db).get_user_by_email(email_from_jwt)
    if user.admin:
        await UserRoomCruds(db=db).leave_room(user_id)
        return {
            "result": "leaved successfully"
        }
    raise HTTPException(status_code=400, detail="No permissions to do this")
