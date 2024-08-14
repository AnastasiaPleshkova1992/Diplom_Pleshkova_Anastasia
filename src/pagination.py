from typing import TypeVar

from fastapi import Query
from fastapi_pagination import Page, Params
# from fastapi_pagination.customization import CustomizedPage, UseParams

T = TypeVar('T')


class PaginatedMetaDataModel(Params):
    total: int | None = Query(10, description='Total')
    page: int | None = Query(1, ge=1, description='Page')
    size: int | None = Query(10,ge=1,  description='Size')


# PaginatePage = CustomizedPage[
#     Page[T],
#     UseParams(PaginatedMetaDataModel)
# ]
