from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.exeptions import ExceptionResponseModel
from src.users.models import User, City
from src.admin.schemas import PrivateCreateUserModel, PrivateUpdateUserModel
from src.users.service import get_user_by_id
from fastapi import Request

from src.users.service import get_current_user


async def get_current_admin_user(session: AsyncSession, request: Request):
    current_user = await get_current_user(session, request)
    if current_user.is_admin:
        return current_user.is_admin
    raise ExceptionResponseModel(code=403, message="Administrator only")


async def get_users(session: AsyncSession, page: int, size: int):
    query = select(User)
    users = await session.execute(query)
    return users.scalars().all()[page : size + page]


async def get_cities(session: AsyncSession):
    query = select(City)
    cities = await session.execute(query)
    return cities.scalars().all()


async def create_user(session: AsyncSession, user_create: PrivateCreateUserModel):
    user = User(**user_create.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def update_user(
    session: AsyncSession, pk: int, user_update: PrivateUpdateUserModel
):
    query = update(User).where(User.id == pk).values(**user_update.model_dump())
    try:
        await session.execute(query)
        await session.commit()
    except Exception as e:
        print(e)
        raise ExceptionResponseModel(code=400, message="Invalid data")
    result = await get_user_by_id(session, pk)
    return result


async def delete_user(session: AsyncSession, pk: int):
    user = await get_user_by_id(session, pk)
    await session.delete(user)
    await session.commit()
