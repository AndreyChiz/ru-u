from fastapi import APIRouter, Depends, status
from .schema import (
    PaletteRequestSchema,
    PaletteRenameRequest,
    UserPalettesRsponse,
    PaletteResponseSchema,
)
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
from src.database import get_async_session


router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    description="Создание плитры",
    response_model=PaletteResponseSchema,
)
async def crate_palette(
    palette: PaletteRequestSchema,
    user_data=Depends(get_data_from_token),
    session=Depends(get_async_session),
):
    try:
        created_palette = await create_new_palette(session=session, palete_name=palette.name, user_id=user_data["id"])
        return created_palette
    except IntegrityError:
        raise PaletteAlreadyExistException


@router.get("/{palette_id}", description="получение палитры по идентификатору")
async def get_palette(
    palette_id: int,
    user_data=Depends(get_data_from_token),
    session=Depends(get_async_session),
):
    if palette := await get_palette_by_id(session, palette_id, user_data["id"]):
        return palette
    raise PaletteNotFoundException


@router.get(
    "/", description="получение коллекции палитр", response_model=UserPalettesRsponse
)
async def get_my_paletts(
    user_data=Depends(get_data_from_token),
    session=Depends(get_async_session),
):
    result = await get_paletts_by_user_id(session, user_data["id"])
    return result


@router.delete(
    "/{palette_id}",
    response_model=PaletteResponseSchema,
    description="удаление палитры.",
)
async def delete_palette_by_id(
    palette_id: int,
    user_data=Depends(get_data_from_token),
    session=Depends(get_async_session),
):
    result = await drop_palette(session, palette_id, user_data["id"])
    if not result:
        raise PaletteNotFoundException
    return result


@router.put(
    "/rename", response_model=PaletteResponseSchema, description="изменение палитры"
)
async def rename_palette(
    request_data: PaletteRenameRequest,
    user_data=Depends(get_data_from_token),
    session=Depends(get_async_session),
):
    result = await set_palette_name(session, request_data.model_dump(), user_data["id"])
    if not result:
        raise PaletteNotFoundException
    return result
