from sqlalchemy import (
    DateTime,
    Identity,
    Integer,
    LargeBinary,
    String,

)

from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.schema import ForeignKey


from .base import Base, CommonDataTypes

# Цвет
# - Идентификатор
# - Идентификатор палитры
# - HEX цвета. Устанавливается пользователем при создании или изменении.
# - Название. Генерируется автоматически на основании HEX при создании или изменении.
# Дополнительно


class Color(Base):
    palette_id: Mapped[str] = mapped_column(String(32), nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user.id", ondelete="CASCADE"),
    )


