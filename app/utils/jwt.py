from datetime import datetime, timedelta
from typing import Union, Any

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

from app.config import settings
from app.cruds.user_cruds import UserCruds
from app.database import db

token_auth_scheme = HTTPBearer()


def create_access_token(email: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "email": str(email)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET, settings.MY_ALGORITHMS)
    return encoded_jwt


async def get_login_from_token(token: str = Depends(token_auth_scheme)):
    pyload_from_me = VerifyToken(token.credentials).verify_my()
    if pyload_from_me.get("status"):
        raise HTTPException(status_code=400, detail="token verification failed")
    user_now = await UserCruds(db=db).get_user_by_email(str(pyload_from_me.get("email")))
    if str(pyload_from_me.get("email")) != str(user_now.email):
        raise HTTPException(status_code=400, detail="token verification failed")
    return pyload_from_me.get("email")


def set_up():
    config = {
        "MY_ALGORITHMS": settings.MY_ALGORITHMS,
        "SECRET": settings.SECRET
    }
    return config


class VerifyToken():
    """Does all the token verification using PyJWT"""

    def __init__(self, token):
        self.token = token
        self.config = set_up()

    def verify_my(self):
        try:
            payload = jwt.decode(
                self.token,
                self.config["SECRET"],
                algorithms=[self.config["MY_ALGORITHMS"]],
            )
        except Exception as e:
            return {"status": "error", "message": str(e)}

        return payload
