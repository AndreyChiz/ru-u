from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.schema import ForeignKey
from sqlalchemy import Index

from src.database import Base


# Палитра
# - Идентификатор
# - Название. Устанавливается пользователем при создании или изменении.


class Palette(Base):
    name: Mapped[str] = mapped_column(String(32), nullable=False)
    user_id = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (Index("idx_palette_user_name", "user_id", "name", unique=True),)

    user = relationship("User", back_populates="palettes")

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


# ####
# import aiohttp
# import asyncio


# class ColorAPI:
#     @classmethod
#     async def get_color_name_async(cls, hex_color):
#         url = f"https://www.thecolorapi.com/id?hex={hex_color}"
#         async with aiohttp.ClientSession() as session:
#             async with session.get(url) as response:
#                 data = await response.json()
#                 color_name = data.get("name", {}).get("value")
#                 return color_name

#     @classmethod
#     async def get_color_name(cls, hex_color):
#         return await cls.get_color_name_async(hex_color)


# async def main():
#     hex_color = "FF0000"
#     color_name = await ColorAPI.get_color_name(hex_color)
#     print(f"The color name for {hex_color} is: {color_name}")


# asyncio.run(main())
