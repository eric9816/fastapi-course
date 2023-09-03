from fastapi import Request, Depends
from jose import jwt, JWTError
from app.config import settings
from datetime import datetime
from app.users.service import UserService
from app.exceptions import *


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise UserTokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=settings.AUTH_ALGORYTHM
        )
    except JWTError:
        raise UserIncorrectTokenException

    expire: str = payload.get("exp")
    if (not expire) and (int(expire) < datetime.utcnow().timestamp()):
        raise UserExpiredTokenException

    user_id: str = payload.get("sub")
    if not user_id:
        raise UserNotExists

    user = await UserService.find_by_id(int(user_id))
    if not user:
        raise UserNotExists
    return user