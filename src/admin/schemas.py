from typing import List

from fastapi import Body
from pydantic import BaseModel, Field

from src.pagination import PaginatedMetaDataModel
from src.users.schemas import UsersListElementModel


class PrivateCreateUserModel(BaseModel):
    first_name: str = Field(title='First Name')
    last_name: str = Field(title='Last Name')
    other_name: str | None = Field(title='Other Name', default=None)
    email: str = Field(title='Email')
    phone: str | None = Field(title='Phone', default=None)
    birthday: str | None = Field(title='Birthday', format='date')
    city: int | None = Field(title='City', default=None)
    additional_info: str | None = Field(title='Additional Info', default=None)
    is_admin: bool = Field(title='Is Admin', default=False)
    password: str = Field(title='Password')


class PrivateDetailUserResponseModel(BaseModel):
    id: int | None = Field (title='Id')
    first_name: str | None = Field(title='First Name')
    last_name: str | None = Field(title='Last Name')
    other_name: str | None = Field(title='Other Name')
    email: str | None = Field(title='Email')
    phone: str | None = Field(title='Phone')
    birthday: str | None = Field(title='Birthday', format='date')
    city: int | None = Field(title='City')
    additional_info: str | None = Field(title='Additional Info')
    is_admin: bool | None = Field(title='Is Admin', default=False)


class PrivateUpdateUserModel(BaseModel):
    id: int = Field(title='Id')
    first_name: str | None = Field(title='First Name')
    last_name: str | None = Field(title='Last Name')
    other_name: str | None = Field(title='Other Name')
    email: str | None = Field(title='Email')
    phone: str | None = Field(title='Phone')
    birthday: str | None = Field(title='Birthday', format='date')
    city: int | None = Field(title='City')
    additional_info: str | None = Field(title='Additional Info')
    is_admin: bool | None = Field(title='Is Admin', default=False)


class CitiesHintModel(BaseModel):
    id: int = Field(title='ID')
    name: str = Field(title='Name')


class PrivateUsersListHintMetaModel(BaseModel):
    city: List[CitiesHintModel] = Body(title='City')


class PrivateUsersListMetaDataModel(BaseModel):
    pagination: PaginatedMetaDataModel = Body(...)
    hint: PrivateUsersListHintMetaModel = Body(...)


class PrivateUsersListResponseModel(BaseModel):
    data: List[UsersListElementModel] = Body(title='Data')
    meta: List[PrivateUsersListMetaDataModel] = Body(title='Meta')
