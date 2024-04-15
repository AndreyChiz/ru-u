from sqlalchemy import and_, delete, select
from src.database import session_factory
from .models import Palette
from src.config import settings
from jose import jwt
from src.database import in_session


import bcrypt


@in_session
async def create_new_palette(session, palete_data: dict):
    new_palette = Palette(**palete_data)
    session.add(new_palette)
    return new_palette


@in_session
async def get_palette_by_id(session, palette_id: int, user_id: int):
    stmt = select(Palette).where(
        and_(
            Palette.user_id == user_id,
            Palette.id == palette_id,
        )
    )

    result = await session.execute(stmt)
    return result.scalars().first()


@in_session
async def get_paletts_by_user_id(session, user_id: int):
    stmt = select(Palette).where(Palette.user_id == user_id)
    result = await session.execute(stmt)
    return result.scalars().all()


@in_session
async def drop_palette(session, palette_id: int, user_id: int):
    stmt = select(Palette).where(
    and_(
        Palette.user_id == user_id,
        Palette.id == palette_id,
        )
    )
    palete_to_delete = await session.scalar(stmt)
    await session.delete(palete_to_delete)

    return palete_to_delete


@in_session
async def set_palette_name(session, changes: dict, user_id: int):
    stmt = select(Palette).where(
        and_(
            Palette.user_id == user_id,
            Palette.name == changes["name"],
        )
    )
    palete_to_rename = await session.scalar(stmt)
    palete_to_rename.name = changes.get("new_name")
    return palete_to_rename
