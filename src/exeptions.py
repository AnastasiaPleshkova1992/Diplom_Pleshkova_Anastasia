from pydantic import BaseModel


class ExceptionResponseModel(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message


class ErrorResponseModel(BaseModel):
    code: int
    message: str


class CodelessErrorResponseModel(BaseModel):
    message: str
