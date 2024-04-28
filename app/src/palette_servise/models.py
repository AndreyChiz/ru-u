from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.schema import ForeignKey
from sqlalchemy import Index
from typing import List
from src.database import Base


# Палитра
# - Идентификатор
# - Название. Устанавливается пользователем при создании или изменении.


class Palette(Base):
    name: Mapped[str] = mapped_column(String(32), nullable=False)
    user_id = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (Index("idx_palette_user_name", "user_id", "name", unique=True),)

    user = relationship("User", back_populates="palettes")

    colors: Mapped[List["Color"]] = relationship(
    back_populates="palette", lazy="selectin"
)