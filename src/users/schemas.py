from pydantic import BaseModel, ConfigDict, Field

from src.pagination import PaginatedMetaDataModel


class UpdateUserModel(BaseModel):
    first_name: str | None = Field(title='First Name')
    last_name: str | None = Field(title='Last Name')
    other_name: str | None = Field(title='Other Name')
    email: str | None = Field(title='Email')
    phone: str | None = Field(title='Phone')
    birthday: str | None = Field(title='Birthday', format='%Y-%m-%d')


class CurrentUserResponseModel(BaseModel):
    first_name: str | None = Field(title='First Name')
    last_name: str | None = Field(title='Last Name')
    other_name: str | None = Field(title='Other Name')
    email: str | None = Field(title='Email')
    phone: str | None = Field(title='Phone')
    birthday: str | None = Field(title='Birthday', format='%Y-%m-%d')
    is_admin: bool | None = Field(title='Is Admin', default=False)


class UpdateUserResponseModel(BaseModel):
    id: int = Field(title='Id')
    first_name: str = Field(title='First Name')
    last_name: str = Field(title='Last Name')
    other_name: str = Field(title='Other Name')
    email: str = Field(title='Email')
    phone: str = Field(title='Phone')
    birthday: str = Field(title='Birthday', format='%Y-%m-%d')


class UsersListElementModel(BaseModel):
    id: int = Field(title='Id')
    first_name: str = Field(title='First Name')
    last_name: str = Field(title='Last Name')
    email: str = Field(title='Email')


class UsersListMetaDataModel(BaseModel):
    pagination: PaginatedMetaDataModel


class UsersListResponseModel(BaseModel):
    data: UsersListElementModel = Field(title='Data')
    meta: UsersListMetaDataModel
