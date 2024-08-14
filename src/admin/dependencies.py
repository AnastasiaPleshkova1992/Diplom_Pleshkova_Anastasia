from fastapi import Request, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.service import get_current_user


async def get_current_admin_user(session: AsyncSession, request: Request):
    current_user = await get_current_user(session, request)
    if current_user.is_admin:
        return current_user.is_admin
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав!"
    )
