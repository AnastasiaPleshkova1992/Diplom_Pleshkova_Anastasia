from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.annotation import Annotated

from src import db_helper
from src.admin.schemas import (
    PrivateCreateUserModel,
    PrivateDetailUserResponseModel,
    PrivateUpdateUserModel,
    PrivateUsersListResponseModel,
)
from src.admin.service import (
    create_user,
    delete_user,
    update_user,
    get_users,
    get_cities,
    get_current_admin_user,
)
from src.exeptions import ErrorResponseModel, CodelessErrorResponseModel
from src.users.service import get_user_by_id

router = APIRouter(prefix="/private/users", tags=["admin"])


@router.get(
    "",
    summary="Постраничное получение кратких данных обо всех пользователях",
    responses={
        400: {"model": ErrorResponseModel},
        401: {"model": CodelessErrorResponseModel},
        403: {"model": CodelessErrorResponseModel},
    },
    response_model=PrivateUsersListResponseModel
)
async def private_users_get(
    page: int,
    size: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    request: Request = Request,
):
    """Здесь находится вся информация, доступная пользователю о других пользователях"""
    await get_current_admin_user(session=session, request=request)
    users_list = await get_users(session=session, page=page, size=size)
    cities_list = await get_cities(session=session)
    total = len(users_list)
    pagination = {"total": total, "page": page, "size": size}
    return {
        "data": users_list,
        "meta": [{"pagination": pagination, "hint": cities_list}]}


@router.post(
    "",
    summary="Создание пользователя",
    response_model=PrivateDetailUserResponseModel,
    status_code=201,
    responses={
        400: {"model": ErrorResponseModel},
        401: {"model": CodelessErrorResponseModel},
        403: {"model": CodelessErrorResponseModel},
    },
)
async def private_users_post(
    user_create: PrivateCreateUserModel = Annotated[Depends(get_current_admin_user)],
    session: AsyncSession = Depends(db_helper.session_getter),
    request: Request = Request,
) -> PrivateDetailUserResponseModel:
    """Здесь возможно занести в базу нового пользователя с минимальной информацией о нем"""
    await get_current_admin_user(session=session, request=request)
    return await create_user(session=session, user_create=user_create)


@router.get(
    "/{pk}",
    summary="Детальное получение информации о пользователе",
    response_model=PrivateDetailUserResponseModel,
    responses={
        400: {"model": ErrorResponseModel},
        401: {"model": CodelessErrorResponseModel},
        403: {"model": CodelessErrorResponseModel},
        404: {"model": CodelessErrorResponseModel},
    },
)
async def private_users__pk__get(
    pk: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    request: Request = Request,
) -> PrivateDetailUserResponseModel:
    """Здесь администратор может увидеть всю существующую пользовательскую информацию"""
    await get_current_admin_user(session=session, request=request)
    user = await get_user_by_id(session=session, pk=pk)
    return user


@router.delete(
    "/{pk}",
    summary="Удаление пользователя",
    status_code=204,
    responses={
        401: {"model": CodelessErrorResponseModel},
        403: {"model": CodelessErrorResponseModel},
    },
)
async def private_users__pk__delete(
    pk: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    request: Request = Request,
):
    """Удаление пользователя"""
    result = await get_current_admin_user(session=session, request=request)
    if result:
        print("Cool")
    await delete_user(pk=pk, session=session)


@router.patch(
    "/{pk}",
    summary="Изменение информации о пользователе",
    response_model=PrivateDetailUserResponseModel,
    responses={
        400: {"model": ErrorResponseModel},
        401: {"model": CodelessErrorResponseModel},
        403: {"model": CodelessErrorResponseModel},
        404: {"model": CodelessErrorResponseModel},
    },
)
async def private_users__pk__patch(
    pk: int,
    user_update: PrivateUpdateUserModel,
    session: AsyncSession = Depends(db_helper.session_getter),
    request: Request = Request,
) -> PrivateDetailUserResponseModel:
    """Здесь администратор может изменить любую информацию о пользователе"""
    result = await get_current_admin_user(session=session, request=request)
    if result:
        print("Cool")
    return await update_user(pk=pk, user_update=user_update, session=session)
