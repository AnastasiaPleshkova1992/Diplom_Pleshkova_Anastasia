from fastapi import HTTPException


class ErrorResponseModel(Exception):
    """status_code:400,
    description: Bad Request"""
    def __init__(self, code, message):
        self.code = code
        self.message = message


class CodelessErrorResponseModel(Exception):
    """status_code: 401,
    description: Unauthorized
    status_code: 403,
    description: Forbidden
    status_code: 404,
    description: Not Found
    """
    def __init__(self, code, message):
        self.code = code
        self.message = message
