from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.config import settings
from src.database import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_helper.dispose()


main_app = FastAPI(**settings.model_dump(), lifespan=lifespan)

if __name__ == '__main__':
    uvicorn.run(
        'main:main_app',
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
