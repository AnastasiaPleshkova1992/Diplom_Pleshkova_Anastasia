from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi_pagination import add_pagination

from src.database import db_helper
from src.config import settings
from src.users.routers import router as users_router
from src.admin.routers import router as admin_router
from src.auth.routers import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_helper.dispose()


main_app = FastAPI(**settings.model_dump(), lifespan=lifespan)

main_app.include_router(auth_router)
main_app.include_router(users_router)
main_app.include_router(admin_router)

add_pagination(main_app)

if __name__ == '__main__':
    uvicorn.run(
        'main:main_app',
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
