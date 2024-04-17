from .models import Color
import aiohttp
from src.exceptions import ColorNameRequestException
from src.database import in_session
from src.auth_service.models import User
from src.palette_servise.models import Palette
from sqlalchemy.exc import IntegrityError


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


@in_session
async def create_new_color(session, palette_id: int, color_hex: bytes):

    color_name = await _get_color_name_async(color_hex)

    new_color = Color(palette_id=palette_id, color_hex=color_hex, name=color_name)
    session.add(new_color)
    return new_color


async def _get_color_by_id(session, user_id: str, palette_id: int, color_id: int):
    if user := await session.get(User, user_id):
        target_palette = None
        for palette in user.palettes:
            if palette.id == palette_id:
                target_palette = palette
                break
    if target_palette:
        for color in target_palette.colors:
            if color.id == color_id:
                return color
    return None




@in_session
async def modify_palette_color_by_id(
    session, palette_id: int, color_id: int, color_hex: bytes, user_id: str
):
    if target_color:= await _get_color_by_id(session, user_id, palette_id, color_id):
        target_color.color_hex = color_hex
        target_color.name = await _get_color_name_async(color_hex)

    return target_color
