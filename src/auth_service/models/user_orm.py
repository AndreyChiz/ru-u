from sqlalchemy.orm import Mapped

from . import Base, CustomType


class User(Base):
    username: Mapped[CustomType.str_32]
    login: Mapped[CustomType.str_32]
    password: Mapped[bytes]



