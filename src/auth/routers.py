from fastapi import APIRouter, HTTPException, status, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src import db_helper
from src.auth.schemas import LoginModel
from src.auth.service import authenticate_user, create_access_token
from src.exeptions import CodelessErrorResponseModel, ErrorResponseModel
from src.users.schemas import CurrentUserResponseModel

router = APIRouter(tags=["Auth"])


@router.post(
    "/login",
    summary="Вход в систему",
    response_model=CurrentUserResponseModel,
    responses={
        400: {
            "description": "Bad Request",
            "content": {"application/json": {"schema": {}}},
        }
    },
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
        raise ErrorResponseModel(code=400, message="Incorrect password or login")
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return check


@router.post("/logout", summary="Выход из системы", status_code=200)
async def logout(response: Response):
    response.delete_cookie(key="users_access_token")
    return {"message": "Пользователь успешно вышел из системы"}
