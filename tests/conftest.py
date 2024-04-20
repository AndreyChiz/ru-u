
from httpx import ASGITransport, AsyncClient
from sqlalchemy import NullPool
from src.config import settings
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
)


import pytest

from sqlalchemy.orm import sessionmaker

from src.app import app
from src.database import get_async_session
from src.database import Base

DATABASE_URL = settings.DATABASE_URL_asyncpg

engine_test = create_async_engine(DATABASE_URL, poolclass=NullPool)

session_factory = sessionmaker(
    bind=engine_test, expire_on_commit=False, class_=AsyncSession
)

Base.metadata.bind = engine_test


async def override_get_async_session():
    async with session_factory() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope="session")
def prepare_database():
    import os

    print("running migrations..")
    os.system("alembic upgrade head")
    yield
    os.system("alembic downgrade base")



@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


test_files_order = [
    'test_registration.py',
    'test_login.py'
    
]


def pytest_collection_modifyitems(session, config, items):
    items.sort(key=lambda item: test_files_order.index(item.fspath.basename))
