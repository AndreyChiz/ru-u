from typing import Annotated, List
from pydantic import BaseModel, ConfigDict, Field


class ColorRequestSchema(BaseModel):
    color_hex: Annotated[bytes, Field(description="Color HEX")]


class ColorResponseSchema(ColorRequestSchema):
    id: int
    palette_id: int
    color_hex: bytes
    name: str

class ColorsOfPAlette(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )

    colors: List[ColorResponseSchema]
