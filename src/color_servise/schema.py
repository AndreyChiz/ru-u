from typing import Annotated, List
from pydantic import BaseModel, ConfigDict, Field

class ColorRequestSchema(BaseModel):
    color_hex: Annotated[bytes, Field(description="Color HEX")]

