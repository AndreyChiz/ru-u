import asyncio
from typing import AsyncGenerator
from functools import wraps
from httpx import AsyncClient, TestClient
from sqlalchemy import NullPool
from src.config import settings
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession, 
)


import pytest

from sqlalchemy.orm import sessionmaker

from src.app import app
from src.database import Base 

DATABASE_URL = settings.TEST_DATABASE_URL_asyncpg

engine_test = create_async_engine(
    DATABASE_URL,
    echo=True,
    poolclass=NullPool
)

session_factory = sessionmaker(bind=engine_test, expire_on_commit=False, class_=AsyncSession)

Base.metadata.bind = engine_test

def in_test_session(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with session_factory() as session:
            async with session.begin():
                return await func(session, *args, **kwargs)

    return wrapper


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as connection:
        await connection.run_sync(Base.memtadata.create_all)
    yield
    async with engine_test.begin() as connection:
        await connection.run_sync(Base.memtadata.drop_all)


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

client =TestClient()

@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(app, base_url="http://test") as ac:
        yield ac 
