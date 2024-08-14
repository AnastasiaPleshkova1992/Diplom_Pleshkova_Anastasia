from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src import db_helper, User
from src.users.schemas import CurrentUserResponseModel
from src.users.service import get_current_user

router = APIRouter(prefix='/users', tags=['user'])

# @router.patch('/current',
#               summary='Изменение данных пользователя',
#               response_model=UpdateUserResponseModel)
# async def edit_user(
#         user_edit: UpdateUserModel = Depends(fastapi_users.current_user()),
#         session: AsyncSession = Depends(db_helper.session_getter)):
#     """ "Здесь пользователь имеет возможность изменить свои данные"""
#     return await edit_user(user_edit=user_edit, session=session)


@router.get('/current',
            summary='Получение данных о текущем пользователе',
            response_model=CurrentUserResponseModel)
async def current_user(request: Request,
                       session: AsyncSession = Depends(db_helper.session_getter)):
    """Здесь находится вся информация, доступная пользователю о самом себе,
    а так же информация является ли он администратором"""
    return await get_current_user(session=session, request=request)




#
#
# @router.get(
#     '',
#     response_model=PaginatePage[UsersListResponseModel],
#     summary='Постраничное получение кратких данных обо всех пользователях',)
# async def users(session: AsyncSession = Depends(db_helper.session_getter)):
#     """Здесь находится вся информация, доступная пользователю о других пользователях"""
#     users_list = await get_all_users(session=session)
#     return await paginate(session, users_list)
