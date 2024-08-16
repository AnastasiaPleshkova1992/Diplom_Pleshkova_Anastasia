from datetime import datetime, timezone

from fastapi import Request
from jose import jwt, JWTError
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.exeptions import ExceptionResponseModel
from src.users.models import User
from src.config import get_auth_data
from src.users.schemas import UpdateUserModel


async def get_user_by_id(session: AsyncSession, pk: int) -> [User]:
    stmt = select(User).filter(User.id == pk)
    user = await session.scalars(stmt)
    return user.first()


def get_token(request: Request):
    token = request.cookies.get("users_access_token")
    return token


async def get_current_user(session: AsyncSession, request: Request):
    try:
        token = get_token(request)
        if not token:
            raise ExceptionResponseModel(code=401, message="Not logged in")
        auth_data = get_auth_data()
        payload = jwt.decode(
            token, auth_data["secret_key"], algorithms=[auth_data["algorithm"]]
        )
    except JWTError:
        raise ExceptionResponseModel(code=400, message="Invalid token")

    expire = payload.get("exp")
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise ExceptionResponseModel(code=400, message="Token expired")

    user_id = payload.get("sub")
    if not user_id:
        raise ExceptionResponseModel(code=400, message="User not identified")

    user = await get_user_by_id(session, int(user_id))
    if not user:
        raise ExceptionResponseModel(code=401, message="User not found")

    return user


async def update_user(
    session: AsyncSession, user_update: UpdateUserModel, request: Request
):
    query = update(User).values(**user_update.model_dump())
    try:
        await session.execute(query)
        await session.commit()
    except Exception as e:
        print(e)
        raise ExceptionResponseModel(code=400, message="Invalid data")
    result = await get_current_user(session, request)
    return result
