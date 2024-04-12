from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.schema import ForeignKey


from . import Base, CustomType


# Палитра
# - Идентификатор
# - Название. Устанавливается пользователем при создании или изменении.


class Palette(Base):
    name: Mapped[CustomType.str_32] 
    user_id = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
    )
