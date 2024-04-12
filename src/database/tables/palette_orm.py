from sqlalchemy import (
    Integer,
    String,
)

from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.schema import ForeignKey


from .base import Base, CommonDataTypes


# Палитра
# - Идентификатор
# - Название. Устанавливается пользователем при создании или изменении.


class Palette(Base):
    name: Mapped[str] = mapped_column(String(32), nullable=False)
    # user_id: Mapped[int] = mapped_column(
    #     Integer,
    #     ForeignKey("user.id", ondelete="CASCADE"),
    # )
