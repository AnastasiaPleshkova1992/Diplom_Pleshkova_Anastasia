from fastapi import HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import User, City
from src.admin.schemas import PrivateCreateUserModel, PrivateUpdateUserModel
from src.users.service import get_user_by_id


async def get_users(session: AsyncSession, page: int, size: int):
    query = select(User)
    users = await session.execute(query)
    return users.scalars().all()[page: size + page]


async def get_cities(session: AsyncSession):
    query = select(City)
    # cities = await session.execute(query)
    return query


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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data"
        )
    result = await get_user_by_id(session, pk)
    return result


async def delete_user(session: AsyncSession, pk: int):
    user = await get_user_by_id(session, pk)
    await session.delete(user)
    await session.commit()
