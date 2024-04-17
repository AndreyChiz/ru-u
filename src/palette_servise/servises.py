from .models import Palette


from src.database import in_session
from src.auth_service.models import User


async def _get_user_palette_by_id(session, palette_id: int, user_id: int):
    if user := await session.get(User, user_id):
        for palette in user.palettes:
            if palette.id == palette_id:
                return palette


@in_session
async def create_new_palette(session, palete_name: str, user_id: str):
    if user := await session.get(User, user_id):
        new_palette = Palette(name=palete_name, user_id=user_id)
        user.palettes.append(new_palette)
        return new_palette


@in_session
async def get_palette_by_id(session, palette_id: int, user_id: int):
    return await _get_user_palette_by_id(session, palette_id, user_id)


@in_session
async def get_paletts_by_user_id(session, user_id: int):
    palettes = await session.get(User, user_id)
    return palettes


@in_session
async def drop_palette(session, palette_id: int, user_id: int):
    if palette:= await _get_user_palette_by_id(session, palette_id, user_id):
        await session.delete(palette)
        return palette
    return None


@in_session
async def set_palette_name(session, changes: dict, user_id: int):
    user = await session.get(User, user_id)
    if user:
        for palette in user.palettes:
            if palette.name == changes["name"]:
                palette.name = changes["new_name"]
                return palette
