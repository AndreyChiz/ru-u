from typing import Annotated
from sqlalchemy import Identity, Integer
from sqlalchemy.orm import DeclarativeBase, declared_attr, mapped_column, Mapped


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """table name like class name"""
        return f"{cls.__name__.lower()}"
