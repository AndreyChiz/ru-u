from typing import Annotated
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError


from .services import create_user, get_user, create_token, check_password
from .schema import (
    RegisterUserRequestSchema,
    RegisterUserResponseSchema,
    LoginUserRequestSchema,
)


from src.exceptions import UserAlreadyExistException, UserCredantialsException


router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=RegisterUserResponseSchema,
    description="Регистрация пользователя",
)
async def register_user(user_credentials: RegisterUserRequestSchema):
    """New user registration"""
    try:
        created_user = await create_user(user_credentials.model_dump())
        return RegisterUserResponseSchema(
            username=created_user.username, login=created_user.login
        )
    except IntegrityError:
        raise UserAlreadyExistException()


@router.post("/login", description="Автроизация пользователя")
async def login_user(auth_request_data: LoginUserRequestSchema):
    """User loginig"""
    if not (
        user := await get_user(auth_request_data.model_dump())
    ) or not check_password(auth_request_data.password, user.password):
        raise UserCredantialsException
    return JSONResponse(
        content={"message": "login ok"},
        headers={"access_token": f"{create_token(user)}", "token_type": "Bearer"},
    )
