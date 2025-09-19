import logging
from contextlib import asynccontextmanager

import asyncpg
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.config import settings

from ..security import require_api_key
from .routes.organizations import router as organizations_router


@asynccontextmanager
async def setup(app: FastAPI):
    postgres_pool = await asyncpg.create_pool(dsn=settings.db_dsn)
    print("Приложение запущено")

    try:
        yield
    finally:
        await postgres_pool.close()
        print("Приложение остановлено")


app = FastAPI(lifespan=setup, root_path="/", debug=True)
uvicorn_access = logging.getLogger("uvicorn.access")
uvicorn_access.disabled = True

app.add_middleware(
    CORSMiddleware,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers={"*"},
    allow_origins=["*"],
    allow_credentials=True,
)

app.include_router(
    organizations_router,
    prefix="",
    dependencies=[Depends(require_api_key)],
)
