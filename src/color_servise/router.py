from fastapi import APIRouter, Depends, status
from .servises import (
    create_new_color,
    modify_color_by_id,
    get_color_by_id,
    get_colors_of_palette,
    delete_color_by_id,
)
from .schema import ColorRequestSchema, ColorResponseSchema, ColorsOfPAlette
from src.security import get_data_from_token
from src.exceptions import (
    ColorAlreadyExistException,
    ColorNotExistExistException,
    PaletteNotFoundException,
)
from sqlalchemy.exc import IntegrityError
from src.database import get_async_session

router = APIRouter(prefix="/{palette_id}/color")


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    name="создание цвета",
    response_model=ColorResponseSchema,
)
async def crate_color(
    palette_id: int,
    color_data: ColorRequestSchema,
    user_data=Depends(get_data_from_token),
    session=Depends(get_async_session),
):
    try:
        if created_color:= await create_new_color(
            session=session,
            palette_id=palette_id,
            color_hex=color_data.color_hex,
            user_id=user_data["id"],
        ):
            return created_color
        raise PaletteNotFoundException
    except IntegrityError:
        raise ColorAlreadyExistException


@router.get(
    "/{color_id}",
    response_model=ColorResponseSchema,
    name="получение цвета по идентификатору,",
)
async def get_color(
    palette_id: int,
    color_id: int,
    user_data=Depends(get_data_from_token),
    session=Depends(get_async_session),
):
    if color := await get_color_by_id(
        session=session,
        palette_id=palette_id,
        color_id=color_id,
        user_id=user_data["id"],
    ):
        return color
    raise ColorNotExistExistException


@router.get(
    "/",
    response_model=ColorsOfPAlette,
    name="получение коллекции цветов по идентификатору палитры",
)
async def get_colors(
    palette_id: int,
    user_data=Depends(get_data_from_token),
    session=Depends(get_async_session),
):
    if  colors:= await get_colors_of_palette(session=session, user_id=user_data["id"], palette_id=palette_id):
        return colors
    raise PaletteNotFoundException


@router.put("/{color_id}", response_model=ColorResponseSchema, name="изменение цвета")
async def change_color(
    palette_id: int,
    color_id: int,
    color_data: ColorRequestSchema,
    user_data=Depends(get_data_from_token),
    session=Depends(get_async_session),
):
    try:

        modifed_palete = await modify_color_by_id(
            session=session,
            palette_id=palette_id,
            color_id=color_id,
            color_hex=color_data.color_hex,
            user_id=user_data["id"],
        )
        if not modifed_palete:
            raise ColorNotExistExistException
        return modifed_palete

    except IntegrityError:
        raise ColorAlreadyExistException


@router.delete(
    "/{color_id}",
    response_model=ColorResponseSchema,
    name="удаление цвета по id",
)
async def delete_color(
    palette_id: int,
    color_id: int,
    user_data=Depends(get_data_from_token),
    session=Depends(get_async_session),
):
    if color := await delete_color_by_id(
        session=session,
        palette_id=palette_id,
        color_id=color_id,
        user_id=user_data["id"],
    ):
        return color
    raise ColorNotExistExistException
