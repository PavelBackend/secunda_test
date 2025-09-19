import asyncio
import sys
from logging.config import fileConfig
from os.path import abspath, dirname, join

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncConnection, create_async_engine

from api.config import settings

ROOT_PATH = abspath(join(dirname(__file__), "..", ".."))
API_PATH = join(ROOT_PATH, "api")
sys.path.insert(0, API_PATH)

from internal.orm_models.dao import *

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

section = config.config_ini_section
config.set_section_option(section, "DB_HOST", settings.POSTGRES_HOST)
config.set_section_option(section, "DB_PORT", str(settings.POSTGRES_PORT))
config.set_section_option(section, "DB_USER", settings.POSTGRES_USER)
config.set_section_option(section, "DB_NAME", settings.POSTGRES_DB)
config.set_section_option(section, "DB_PASS", settings.POSTGRES_PASSWORD)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = settings.db_dsn
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: AsyncConnection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    async_dsn = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

    connectable = create_async_engine(async_dsn, poolclass=pool.NullPool, echo=True)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


async def run_migrations_online() -> None:
    await run_async_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
