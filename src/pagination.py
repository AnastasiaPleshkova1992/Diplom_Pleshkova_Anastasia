from fastapi import Query
from fastapi_pagination import Params


class PaginatedMetaDataModel(Params):
    total: int | None = Query(description='Total')
    page: int | None = Query(description='Page')
    size: int | None = Query(description='Size')
