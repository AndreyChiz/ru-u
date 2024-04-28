import re
from typing import Annotated
from pydantic import BaseModel, Field, field_validator
from src.exceptions import UserPasswordValidationException, UsernameValidationException

STRONG_PASSWORD_PATTERN = re.compile(
    r"^(?=.*[\d])(?=.*[!_@#$%^&*])[\w!_@#$%^&*]{6,128}$"
)

USER_NAME_VALID = re.compile(r"^[a-zA-Z]+$")

password_type = Annotated[
    str,
    Field(
        description="Password must contain at least one lower character, one upper character, digit or special symbol"
    ),
]

username_type = Annotated[
    str,
    Field(
        min_length=3,
        max_length=32,
        description="Username must contain at least only letters",
    ),
]


login_type = Annotated[str, Field(max_length=32)]


def valid_password(password: str) -> str:
    if not re.match(STRONG_PASSWORD_PATTERN, password):
        raise UserPasswordValidationException
    return password


def valid_username(username: str) -> str:
    if not re.match(USER_NAME_VALID, username):
        raise UsernameValidationException
    return username


class RegisterUserResponseSchema(BaseModel):
    username: username_type
    login: login_type

    @field_validator("username", mode="after")
    @classmethod
    def validate_username(cls, username: str) -> str:
        return valid_username(username)


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


class LoginResponseSchema(BaseModel):
    message: str
