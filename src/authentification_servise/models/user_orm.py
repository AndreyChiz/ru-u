from sqlalchemy import LargeBinary, String
from sqlalchemy.orm import mapped_column, Mapped

from . import Base


class User(Base):
    username: Mapped[str] = mapped_column(String(32), nullable=False)
    login: Mapped[str] = mapped_column(String(32), nullable=False)
    password: Mapped[LargeBinary] = mapped_column(LargeBinary)
