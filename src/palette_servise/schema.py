from typing import Annotated, List
from pydantic import BaseModel, Field


class PaletteRequestSchema(BaseModel):
    name: Annotated[str, Field(max_length=32)]


class PaletteRenameRequest(PaletteRequestSchema):
    new_name: Annotated[str, Field(max_length=32)]


class PaletteSchema(PaletteRequestSchema):
    id: int


class UserPalettesRsponse(BaseModel):
    id: int
    username: str
    login: str
    palettes: List[PaletteSchema]
