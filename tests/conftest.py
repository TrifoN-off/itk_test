from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)
from testcontainers.postgres import PostgresContainer

from app.database import Base, get_db
from app.main import app

CUSTOM_BALANCE = 5000
CONCURRENT_OPERATIONS_COUNT = 10
DEPOSIT_OPERATIONS_COUNT = 7
WITHDRAW_OPERATIONS_COUNT = 12
OPERATION_AMOUNT = 150


@pytest.fixture
def postgres_container():
    """Создание контейнера PostgreSQL."""
    with PostgresContainer('postgres:13') as postgres:
        yield postgres


@pytest_asyncio.fixture
async def db_engine(
    postgres_container: PostgresContainer,
) -> AsyncGenerator[AsyncEngine, None]:
    """Создание подключения к базе данных."""
    db_url = postgres_container.get_connection_url().replace(
        "postgresql+psycopg2://", "postgresql+asyncpg://"
    )
    engine = create_async_engine(db_url, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield engine
    finally:
        await engine.dispose()


@pytest_asyncio.fixture
async def session_factory(
    db_engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    """Создание фабрики сессий."""
    return async_sessionmaker(
        bind=db_engine, class_=AsyncSession, expire_on_commit=False
    )


@pytest_asyncio.fixture
async def client(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncClient, None]:
    """Создание тестового клиента."""
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        async with session_factory() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url='http://test'
    ) as client:
        yield client
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def wallet(client: AsyncClient) -> dict:
    """Создание кошелька."""
    resp = await client.post('/api/v1/wallets', json={})
    return resp.json()
