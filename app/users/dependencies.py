import datetime

from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError

from app.config import settings
from app.users.dao import UserDAO
from app.exceptions import (TokenAbsentException, TokenExpiredException,
                            IncorrectTokenFormatException, UserNotFoundException)


def get_token(request: Request) -> str:
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except JWTError:
        raise IncorrectTokenFormatException
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.datetime.utcnow().timestamp()):
        raise TokenExpiredException
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserNotFoundException
    user = await UserDAO.find_by_id(int(user_id))
    if not user:
        raise UserNotFoundException
    return user
