from typing import Annotated
from pydantic import BaseModel, Field


class PaletteRequestSchema(BaseModel):
    name: Annotated[str, Field(max_length=32)]


class PaletteRenameRequest(PaletteRequestSchema):
    new_name: Annotated[str, Field(max_length=32)]
