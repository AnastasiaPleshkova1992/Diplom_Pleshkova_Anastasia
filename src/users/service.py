from datetime import datetime, timezone
from typing import Optional

from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import User, City
from src.config import get_auth_data
from src.users.schemas import UpdateUserModel


async def get_user_by_id(session: AsyncSession, pk: int) -> Optional[User]:
    stmt = select(User).filter(User.id == pk)
    user = await session.scalars(stmt)
    return user.first()


def get_token(request: Request):
    token = request.cookies.get("users_access_token")
    return token


async def get_current_user(session: AsyncSession, request: Request):
    # if not token:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token not found')
    try:
        token = get_token(request)
        auth_data = get_auth_data()
        payload = jwt.decode(
            token, auth_data["secret_key"], algorithms=[auth_data["algorithm"]]
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен не валидный!"
        )

    expire = payload.get("exp")
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен истек"
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Не найден ID пользователя"
        )

    user = await get_user_by_id(session, int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    return user


async def update_user(session: AsyncSession,
                      user_update: UpdateUserModel,
                      request: Request):
    query = update(User).values(**user_update.model_dump())
    try:
        await session.execute(query)
        await session.commit()
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data"
        )
    result = await get_current_user(session, request)
    return result
