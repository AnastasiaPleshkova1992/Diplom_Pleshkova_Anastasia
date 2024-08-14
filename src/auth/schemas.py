from pydantic import BaseModel, Field


class LoginModel(BaseModel):
    login: str = Field(title='Login')
    password: str = Field(title='Password')
