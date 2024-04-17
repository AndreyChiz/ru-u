from typing import Annotated, List
from pydantic import BaseModel, ConfigDict, Field


class PaletteRequestSchema(BaseModel):
    name: Annotated[str, Field(max_length=32)]


class PaletteRenameRequest(PaletteRequestSchema):
    new_name: Annotated[str, Field(max_length=32)]


class PaletteSchema(PaletteRequestSchema):
    id: int


class UserPalettesRsponse(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )

    id: int = Field(alias="user_id")
    username: str
    login: str
    palettes: List[PaletteSchema]
