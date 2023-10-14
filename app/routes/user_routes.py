from fastapi import APIRouter, Depends
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from app.cruds.user_cruds import UserCruds
from app.database import db
from app.schemas.user_schemas import *
from app.utils.jwt import create_access_token, get_login_from_token

router = APIRouter()


@router.post("/login/", tags=["Login"])
async def user_login(email: str, password: str):
    db_user = await UserCruds(db=db).get_user_by_email(email)
    if db_user:
        if db_user.password == password:
            response = JSONResponse(status_code=200, content={
                "access_token": create_access_token(db_user.email)
            })
            return response
        else:
            raise HTTPException(status_code=400, detail="Bad password or email")
    raise HTTPException(status_code=400, detail="No such user")


@router.post("/user/register/", tags=["User"])
async def add_user(new_user: UserCreate, email_from_jwt: str = Depends(get_login_from_token)):
    user = await UserCruds(db=db).get_user_by_email(email_from_jwt)
    if user.admin:
        await UserCruds(db=db).create_user(new_user)
        return {
            "result": "user added successfully"
        }
    raise HTTPException(status_code=400, detail="No permissions to do this")


@router.delete("/user/delete/", tags=["User"])
async def delete_user(email: str, email_from_jwt: str = Depends(get_login_from_token)):
    user = await UserCruds(db=db).get_user_by_email(email_from_jwt)
    if user.admin:
        await UserCruds(db=db).delete_user(email)
        return {
            "result": "user deleted successfully"
        }
    raise HTTPException(status_code=400, detail="No permissions to do this")
