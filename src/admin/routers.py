from fastapi import APIRouter, Depends, Request
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.annotation import Annotated

from src import db_helper, User
from src.admin.dependencies import get_current_admin_user
from src.admin.schemas import (
    PrivateCreateUserModel,
    PrivateDetailUserResponseModel,
    PrivateUpdateUserModel, PrivateUsersListResponseModel,
)
from src.admin.service import (
    create_user,
    delete_user,
    update_user, get_users, get_cities,
)
from src.pagination import PaginatedMetaDataModel
from src.users.service import get_user_by_id

router = APIRouter(prefix="/private/users", tags=["admin"])


@router.get('',
            summary='Постраничное получение кратких данных обо всех пользователях',
            response_model=PrivateUsersListResponseModel)
async def private_users_get(
        page: int,
        size: int,
        session: AsyncSession = Depends(db_helper.session_getter)
) -> PrivateUsersListResponseModel:
    """Здесь находится вся информация, доступная пользователю о других пользователях"""
    users_list = await get_users(session=session)
    paginate_list = await paginate(session, users_list, page=page, size=size)

    return paginate_list



@router.post(
    "", summary="Создание пользователя", response_model=PrivateDetailUserResponseModel
)
async def private_users_post(
    user_create: PrivateCreateUserModel = Annotated[Depends(get_current_admin_user)],
    session: AsyncSession = Depends(db_helper.session_getter),
) -> PrivateDetailUserResponseModel:
    """Здесь возможно занести в базу нового пользователя с минимальной информацией о нем"""
    return await create_user(session=session, user_create=user_create)


@router.get(
    "/{pk}",
    summary="Детальное получение информации о пользователе",
    response_model=PrivateDetailUserResponseModel,
    # dependencies=[Depends(get_current_admin_user)]
)
async def private_users__pk__get(
    pk: int, session: AsyncSession = Depends(db_helper.session_getter)
):
    """Здесь администратор может увидеть всю существующую пользовательскую информацию"""
    user = await get_user_by_id(session=session, pk=pk)
    return user


@router.delete("/{pk}", summary="Удаление пользователя")
async def private_users__pk__delete(
    pk: int, session: AsyncSession = Depends(db_helper.session_getter)
):
    """Удаление пользователя"""
    await delete_user(pk=pk, session=session)


@router.patch(
    "/{pk}",
    summary="Изменение информации о пользователе",
    response_model=PrivateDetailUserResponseModel,
)
async def private_users__pk__patch(
    pk: int,
    user_update: PrivateUpdateUserModel,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Здесь администратор может изменить любую информацию о пользователе"""
    return await update_user(pk=pk, user_update=user_update, session=session)
