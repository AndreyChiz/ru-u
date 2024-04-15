from fastapi import APIRouter, status

router = APIRouter()


# Цвета существуют только в рамках палитр. Пользователь может работать только с его палитрами.


@router.post("/", name="создание цвета")
async def crate_color(): ...


@router.get("/{id}", name="получение цвета по идентификатору,")
async def regcrate_color(): ...


@router.get(
    "/{palette_id}", name="получение коллекции цветов по идентификатору палитры"
)
async def regcrate_color(): ...


@router.delete("/{id}", name="удаление цвета")
async def regcrate_color(): ...


@router.put("/{id}", name="изменение цвета")
async def regcrate_color(): ...
