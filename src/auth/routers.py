from fastapi import APIRouter, HTTPException, status, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src import db_helper, User
from src.admin.schemas import PrivateCreateUserModel
from src.auth.schemas import LoginModel
from src.auth.service import authenticate_user, create_access_token, get_password_hash, get_user_by_login
from src.users.schemas import CurrentUserResponseModel

router = APIRouter(tags=['Auth'])


@router.post("/login",
             summary="Вход в систему",
             response_model=CurrentUserResponseModel)
async def auth_user(response: Response,
                    user_data: LoginModel,
                    session: AsyncSession = Depends(db_helper.session_getter)):
    """После успешного входа в систему необходимо установить Cookies для пользователя"""
    check = await authenticate_user(session=session, login=user_data.login, password=user_data.password)
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Неверная почта или пароль')
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return check


@router.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'message': 'Пользователь успешно вышел из системы'}
