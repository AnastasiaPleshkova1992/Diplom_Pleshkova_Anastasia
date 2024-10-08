from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src import db_helper
from src.admin.service import get_users
from src.exeptions import ErrorResponseModel, CodelessErrorResponseModel

from src.users.schemas import (
    CurrentUserResponseModel,
    UpdateUserResponseModel,
    UpdateUserModel, UsersListResponseModel,
)
from src.users.service import get_current_user, update_user

router = APIRouter(prefix="/users", tags=["user"])


@router.get(
    "/current",
    summary="Получение данных о текущем пользователе",
    response_model=CurrentUserResponseModel,
    responses={
        400: {"model": ErrorResponseModel},
        401: {"model": CodelessErrorResponseModel},
    },
)
async def current_user(
    request: Request, session: AsyncSession = Depends(db_helper.session_getter)
):
    """Здесь находится вся информация, доступная пользователю о самом себе,
    а так же информация является ли он администратором"""
    return await get_current_user(session=session, request=request)


@router.patch(
    "/current",
    summary="Изменение данных пользователя",
    response_model=UpdateUserResponseModel,
    responses={
        400: {"model": ErrorResponseModel},
        401: {"model": CodelessErrorResponseModel},
        404: {"model": CodelessErrorResponseModel},
    },
)
async def edit_user(
    request: Request,
    user_update: UpdateUserModel,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Здесь пользователь имеет возможность изменить свои данные"""
    await get_current_user(session=session, request=request)
    return await update_user(user_update=user_update, session=session, request=request)


@router.get(
    "",
    response_model=UsersListResponseModel,
    summary="Постраничное получение кратких данных обо всех пользователях",
    responses={
        400: {"model": ErrorResponseModel},
        401: {"model": CodelessErrorResponseModel},
    },
)
async def users(
    request: Request,
    page: int,
    size: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Здесь находится вся информация, доступная пользователю о других пользователях"""
    await get_current_user(session=session, request=request)
    users_list = await get_users(session=session, page=page, size=size)
    total = len(users_list)
    pagination = {"total": total, "page": page, "size": size}
    return {"data": users_list, "meta": [{"pagination": pagination}]}
