from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import HTTPException, status
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src import User
from src.config import get_auth_data
from src.exeptions import ErrorResponseModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    auth_data = get_auth_data()
    encode_jwt = jwt.encode(
        to_encode, auth_data["secret_key"], algorithm=auth_data["algorithm"]
    )
    return encode_jwt


async def get_user_by_login(session: AsyncSession, login: str) -> [User]:
    stmt = select(User).filter(User.login == login)
    user = await session.scalars(stmt)
    return user.first()


async def authenticate_user(session: AsyncSession, login: str, password: str):
    user = await get_user_by_login(session=session, login=login)
    if not user or user.password != password:
        return None
    return user
