from fastapi import APIRouter, Depends, status
from .schema import PaletteRequestSchema, PaletteRenameRequest, UserPalettesRsponse
from .servises import (
    create_new_palette,
    get_palette_by_id,
    get_paletts_by_user_id,
    drop_palette,
    set_palette_name,
)
from src.security import get_data_from_token
from src.exceptions import PaletteAlreadyExistException, PaletteNotFoundException
from sqlalchemy.exc import IntegrityError


router = APIRouter()


@router.post("/", 
             status_code=status.HTTP_201_CREATED,
             description="Создание плитры")
async def crate_palette(
    palette: PaletteRequestSchema, user_data=Depends(get_data_from_token)
):
    try:
        return await create_new_palette(palette.name, user_data["id"])
    except IntegrityError:
        raise PaletteAlreadyExistException


@router.get("/{palette_id}", description="получение палитры по идентификатору")
async def get_palette(palette_id: int, user_data=Depends(get_data_from_token)):
    if palette := await get_palette_by_id(palette_id, user_data["id"]):
        return palette
    raise PaletteNotFoundException


@router.get(
    "/", description="получение коллекции палитр", response_model=UserPalettesRsponse
)
async def get_my_paletts(user_data=Depends(get_data_from_token)):
    result = await get_paletts_by_user_id(user_data["id"])
    return result


@router.delete("/{palette_id}", description="удаление палитры.")
async def delete_palette_by_id(palette_id: int, user_data=Depends(get_data_from_token)):
    result = await drop_palette(palette_id, user_data["id"])
    if not result:
        raise PaletteNotFoundException
    return result


@router.put("/rename", description="изменение палитры")
async def rename_palette(
    request_data: PaletteRenameRequest, user_data=Depends(get_data_from_token)
):
    result = await set_palette_name(request_data.model_dump(), user_data["id"])
    if not result:
        raise PaletteNotFoundException
    return result
