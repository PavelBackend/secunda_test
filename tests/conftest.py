import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import NullPool

from api.config import settings
from api.database import get_async_session
from api.internal.main import app
from api.internal.orm_models.dao import Base

TEST_DATABASE_URL = (
    f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
    f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.TEST_POSTGRES_DB}"
)

test_engine = create_async_engine(TEST_DATABASE_URL, echo=False, poolclass=NullPool)


@pytest_asyncio.fixture(scope="session")
async def setup_database():
    """Create test DB if missing, then set up schema once for the whole session."""
    admin_url = (
        f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
        f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/postgres"
    )
    admin_engine = create_async_engine(admin_url, isolation_level="AUTOCOMMIT")
    async with admin_engine.connect() as conn:
        result = await conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :name"),
            {"name": settings.TEST_POSTGRES_DB},
        )
        if not result.fetchone():
            await conn.execute(text(f'CREATE DATABASE "{settings.TEST_POSTGRES_DB}"'))
    await admin_engine.dispose()

    async with test_engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()


@pytest_asyncio.fixture
async def db_session(setup_database):
    """Each test gets a fresh session; everything is rolled back on teardown."""
    session = AsyncSession(test_engine)
    try:
        yield session
    finally:
        await session.rollback()
        await session.close()


@pytest_asyncio.fixture
async def client(db_session: AsyncSession):
    """HTTP test client with DB session overridden to use the test transaction."""

    async def override_session():
        yield db_session

    app.dependency_overrides[get_async_session] = override_session
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
