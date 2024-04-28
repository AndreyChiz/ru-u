from functools import wraps
from sqlalchemy import Identity, String, BigInteger
from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
    mapped_column,
    Mapped,
    sessionmaker,
)


from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
)

from .config import settings


DATABASE_URL = str(settings.DATABASE_URL_asyncpg)
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)

session_factory = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """table name like class name"""
        return f"{cls.__name__.lower()}"


def in_session(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with session_factory() as session:
            async with session.begin():
                return await func(session, *args, **kwargs)

    return wrapper


async def get_async_session():
    async with session_factory() as session:
        yield session
