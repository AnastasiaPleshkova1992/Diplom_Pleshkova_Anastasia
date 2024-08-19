from fastapi import APIRouter, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src import db_helper, User
from src.auth.schemas import LoginModel
from src.auth.service import (
    authenticate_user,
    create_access_token,
    get_user_by_login,
    get_password_hash,
)
from src.exeptions import ErrorResponseModel, ExceptionResponseModel
from src.users.schemas import CurrentUserResponseModel

router = APIRouter(tags=["Auth"])


@router.post(
    "/register",
    summary="Регистрация нового пользователя",
    response_model=dict,
    responses={400: {"model": ErrorResponseModel}},
)
async def register_user(
    user_data: LoginModel, session: AsyncSession = Depends(db_helper.session_getter)
) -> dict:
    user = await get_user_by_login(login=user_data.login, session=session)
    if user:
        raise ExceptionResponseModel(code=400, message="User already exists")
    user_dict = user_data.dict()
    user_dict["password"] = get_password_hash(user_data.password)
    session.add(User(**user_dict))
    return {"message": "You have successfully registered!"}


@router.post(
    "/login",
    summary="Вход в систему",
    response_model=CurrentUserResponseModel,
    responses={400: {"model": ErrorResponseModel}},
)
async def login(
    response: Response,
    user_data: LoginModel,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> CurrentUserResponseModel:
    """После успешного входа в систему необходимо установить Cookies для пользователя"""
    check = await authenticate_user(
        session=session, login=user_data.login, password=user_data.password
    )
    if check is None:
        raise ExceptionResponseModel(code=400, message="Incorrect password or login")
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return check


@router.post("/logout", summary="Выход из системы", status_code=200)
async def logout(response: Response):
    response.delete_cookie(key="users_access_token")
    return {"message": "Пользователь успешно вышел из системы"}
