from fastapi import APIRouter, Depends
from .schema import PaletteRequestSchema, PaletteRenameRequest
from .services import (
    create_new_palette,
    get_palette_by_id,
    get_paletts_by_user_id,
    drop_palette,
    set_palette_name,
)
from src.security import get_data_from_token
from src.exceptions import PaletteAlreadyExistException, PaletteNotFoundException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

router = APIRouter()
"""
- Методы для работы с палитрами: , , , ,  Пользователь может
  работать только с его палитрами.
"""


@router.post("/", description="Создание плитры")
async def crate_palette(
    palette: PaletteRequestSchema, user_data=Depends(get_data_from_token)
):
    user_id_palette = palette.model_dump()
    user_id_palette["user_id"] = user_data["id"]
    try:
        return await create_new_palette(user_id_palette)
    except IntegrityError:
        raise PaletteAlreadyExistException


@router.get("/{palette_id}", description="получение палитры по идентификатору")
async def get_palette(palette_id: int, user_data=Depends(get_data_from_token)):
    if palette := await get_palette_by_id(palette_id, user_data["id"]):
        return palette
    raise PaletteNotFoundException


@router.get("/", description="получение коллекции палитр")
async def get_my_paletts(user_data=Depends(get_data_from_token)):
    return await get_paletts_by_user_id(user_data["id"])


@router.delete("/{palette_id}", description="удаление палитры.")
async def delete_palette_by_id(palette_id: int, user_data=Depends(get_data_from_token)):
    try:
        return await drop_palette(palette_id, user_data["id"])
    except UnmappedInstanceError:
        raise PaletteNotFoundException


@router.put("/rename", description="изменение палитры")
async def rename_palette(
    request_data: PaletteRenameRequest, user_data=Depends(get_data_from_token)
):
    return await set_palette_name(request_data.model_dump(), user_data["id"])
