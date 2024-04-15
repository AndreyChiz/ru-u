import re
from typing import Annotated
from pydantic import BaseModel, Field, field_validator
from src.exceptions import UserPasswordValidationException

STRONG_PASSWORD_PATTERN = re.compile(
    r"^(?=.*[\d])(?=.*[!_@#$%^&*])[\w!_@#$%^&*]{6,128}$"
)

password_type = Annotated[
        str,
        Field(
            description="Password must contain at least one lower character, one upper character, digit or special symbol"
        ),
    ]
login_type = Annotated[str, Field(max_length=32)]


def valid_password(password: str) -> str:
    if not re.match(STRONG_PASSWORD_PATTERN, password):
        raise UserPasswordValidationException
    return password


class RegisterUserResponseSchema(BaseModel):
    username: Annotated[str, Field(max_length=32)]
    login: login_type


class RegisterUserRequestSchema(RegisterUserResponseSchema):
    password: password_type

    @field_validator("password", mode="after")
    @classmethod
    def valid_password(cls, password: str) -> str:
        return valid_password(password)


class LoginUserRequestSchema(BaseModel):
    login: login_type
    password: password_type

    @field_validator("password", mode="after")
    @classmethod
    def valid_password(cls, password: str) -> str:
        return valid_password(password)
