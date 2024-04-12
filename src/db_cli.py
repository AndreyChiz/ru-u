from typing import Annotated
from sqlalchemy import Identity, String, BigInteger
from sqlalchemy.orm import DeclarativeBase, declared_attr, mapped_column, Mapped, Session


from sqlalchemy.ext.asyncio import create_async_engine

from src.config import settings

DATABASE_URL = str(settings.DATABASE_URL_asyncpg)
engine = create_async_engine(DATABASE_URL)


class CustomType:
    id_type = Annotated[int, mapped_column(BigInteger, Identity(), primary_key=True)]
    str_32 = Annotated[str, mapped_column(String(32))]


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[CustomType.id_type] 

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """table name like class name"""
        return f"{cls.__name__.lower()}"


