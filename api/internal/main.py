import asyncio
from contextlib import asynccontextmanager
import logging
import asyncpg
from api.config import settings
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..security import require_api_key
from .add_mocks import seed
from .routes.organizations import router as organizations_router
from sqlalchemy import text
from api.database import async_session_maker


async def _wait_for_db(dsn: str, tries: int = 30, base_delay: float = 1.0) -> None:
    delay = base_delay
    last_err = None
    for attempt in range(1, tries + 1):
        try:
            conn = await asyncpg.connect(dsn)
            await conn.close()
            print(f"БД доступна (попытка {attempt})")
            return
        except (ConnectionRefusedError, OSError, asyncpg.PostgresConnectionError) as e:
            last_err = e
            print(f"БД не отвечает (попытка {attempt}/{tries}): {e}. Ждём {delay:.1f}с...")
            await asyncio.sleep(delay)
            delay = min(delay * 1.5, 5.0)
    raise RuntimeError(f"Не удалось подключиться к БД после {tries} попыток: {last_err}")


@asynccontextmanager
async def setup(app: FastAPI):
    # await _wait_for_db(settings.db_dsn)
    postgres_pool = await asyncpg.create_pool(dsn=settings.db_dsn)
    print("Приложение запущено")

    # async with async_session_maker() as session:
    #     try:
    #         if not (await session.execute(text("SELECT 1 FROM organization LIMIT 1;"))).first():
    #             print("Таблица organization пуста, запускаем сидер...")
    #             await seed()
    #         else:
    #             print("В таблице organization уже есть данные, сидер не нужен")
    #     except Exception as e:
    #         print(f"Ошибка при проверке базы: {e}")

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
    allow_methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
    allow_headers={"*"},
    allow_origins=["*"],
    allow_credentials=True
)

app.include_router(
    organizations_router,
    prefix="",
    dependencies=[Depends(require_api_key)],
)