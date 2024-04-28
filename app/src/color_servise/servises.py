from .models import Color
import aiohttp
from src.exceptions import ColorNameRequestException
from src.database import in_session
from src.auth_service.models import User
from src.palette_servise.models import Palette
from sqlalchemy.exc import IntegrityError
from src.palette_servise.servises import _get_user_palette_by_id


async def _get_color_name_async(hex_color):
    hex_str = hex_color.decode("utf-8")
    try:
        url = f"https://www.thecolorapi.com/id?hex={hex_str}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                color_name = data.get("name", {}).get("value")
                return color_name
    except Exception:
        raise ColorNameRequestException


async def _get_color_by_id(session, user_id: str, palette_id: int, color_id: int):
    if target_palette := await _get_user_palette_by_id(session, palette_id, user_id):
        for color in target_palette.colors:
            if color.id == color_id:
                return color
    return None


async def get_color_by_id(session, user_id: str, palette_id: int, color_id: int):
    async with session.begin():
        if target_color := await _get_color_by_id(session, user_id, palette_id, color_id):
            return target_color


async def create_new_color(session, palette_id: int, color_hex: bytes, user_id: int):
    async with session.begin():
        if target_palette := await _get_user_palette_by_id(session, palette_id, user_id):
            color_name = await _get_color_name_async(color_hex)
            new_color = Color(palette_id=palette_id, color_hex=color_hex, name=color_name)
            target_palette.colors.append(new_color)
            return new_color


async def modify_color_by_id(
    session, palette_id: int, color_id: int, color_hex: bytes, user_id: str
):
    async with session.begin():
        if target_palette := await _get_user_palette_by_id(session, palette_id, user_id):
            for color in target_palette.colors:
                if color.id == color_id:
                    color.color_hex = color_hex
                    color.name = await _get_color_name_async(color_hex)
                    return color


async def get_colors_of_palette(session, user_id: str, palette_id: int):
    async with session.begin():
        return await _get_user_palette_by_id(session, palette_id, user_id)


async def delete_color_by_id(session, user_id: str, palette_id: int, color_id: int):
    async with session.begin():
        if target_color := await _get_color_by_id(session, user_id, palette_id, color_id):
            await session.delete(target_color)
            return target_color
