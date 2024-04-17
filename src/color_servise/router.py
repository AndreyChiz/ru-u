from fastapi import APIRouter, Depends, status
from .servises import create_new_color, modify_palette_color_by_id
from .schema import ColorRequestSchema
from src.security import get_data_from_token
from src.exceptions import ColorAlreadyExistException, ColorNotExistExistException
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/{palette_id}/color")


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    name="создание цвета",
)
async def crate_color(
    palette_id: int,
    color_data: ColorRequestSchema,
    user_data=Depends(get_data_from_token),
):
    try:
        return await create_new_color(
            palette_id=palette_id,
            color_hex=color_data.color_hex,
        )
    except IntegrityError:
        raise ColorAlreadyExistException


@router.get("/{id}", name="получение цвета по идентификатору,")
async def regcrate_color(): ...


@router.get("/", name="получение коллекции цветов по идентификатору палитры")
async def regcrate_color(): ...


@router.delete("/{id}", name="удаление цвета")
async def regcrate_color(): ...


@router.put("/{color_id}", name="изменение цвета")
async def change_color(
    palette_id: int,
    color_id: int,
    color_data: ColorRequestSchema,
    user_data=Depends(get_data_from_token),
):
    try:

        modifed_palete = await modify_palette_color_by_id(
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
