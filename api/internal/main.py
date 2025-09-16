from contextlib import asynccontextmanager
import logging
import asyncpg
from api.config import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def setup(app: FastAPI):
    postgres_pool = await asyncpg.create_pool(dsn=settings.db_dsn)
    print("Приложение запущено")
    yield
    await postgres_pool.close()
    print("Приложение остановлено")


app = FastAPI(lifespan=setup, root_path="/", debug=True)
uvicorn_access = logging.getLogger("uvicorn.access")
uvicorn_access.disabled = True

app.add_middleware(
    CORSMiddleware,
    allow_methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
    allow_headers={"*"},
    allow_origins=["*"],
    allow_credentials=True
)
