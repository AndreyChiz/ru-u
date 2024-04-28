from typing import List
from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm.attributes import InstrumentedAttribute
from src.database import Base
import aiohttp

# Цвет
# - Идентификатор
# - Идентификатор палитры
# - HEX цвета. Устанавливается пользователем при создании или изменении.
# - Название. Генерируется автоматически на основании HEX при создании или изменении.
# Дополнительно


class Color(Base):

    palette_id = mapped_column(
        ForeignKey("palette.id", ondelete="CASCADE"),
    )
    color_hex: Mapped[bytes]
    name: Mapped[str] 

    palette = relationship("Palette", back_populates="colors")

    __table_args__ = (
        Index("idx_color_name_palette_id", "palette_id", "name", unique=True),
    )
