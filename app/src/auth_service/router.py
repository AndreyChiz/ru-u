from typing import Annotated
from fastapi import APIRouter, status, Response, Depends
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError


from .services import create_user, get_user, create_token, check_password
from .schema import (
    RegisterUserRequestSchema,
    RegisterUserResponseSchema,
    LoginUserRequestSchema,
    LoginResponseSchema,
)


from src.exceptions import UserAlreadyExistException, UserCredantialsException
from src.database import get_async_session

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=RegisterUserResponseSchema,
    description="Регистрация пользователя",
)
async def register_user(
    user_credentials: RegisterUserRequestSchema, session=Depends(get_async_session)
):
    """New user registration"""
    try:
        created_user = await create_user(session, user_credentials.model_dump())
        return created_user
    except IntegrityError:
        raise UserAlreadyExistException()


@router.post(
    "/login", description="Автроизация пользователя", response_model=LoginResponseSchema
)
async def login_user(
    auth_request_data: LoginUserRequestSchema, session=Depends(get_async_session)
):
    """User loginig"""
    if not (
        user := await get_user(session, auth_request_data.login)
    ) or not check_password(auth_request_data.password, user.password):
        raise UserCredantialsException

    response_model = LoginResponseSchema(message="login ok")
    response = JSONResponse(
        content=response_model.model_dump(),
        headers={"access_token": f"{create_token(user)}", "token_type": "Bearer"},
    )

    return response
