from sqlalchemy import select
from .models import User
from src.config import settings
from jose import jwt
from src.database import in_session

import bcrypt


@in_session
async def create_user(session, user_data: dict):
    new_user = User(**user_data)
    new_user.password = hash_password(new_user.password)
    session.add(new_user)
    return new_user


@in_session
async def get_user(session, login: str):
    stmt = select(User).where(User.login == login)
    result = await session.execute(stmt)
    user = result.scalars().first()
    return user




def create_token(user: User):
    KEY: str = settings.JWT_KEY
    ALGORITHM: str = settings.ALGORITHM
    claims = {"username": user.username, "login": user.login, "id": user.id}
    return jwt.encode(claims=claims, key=KEY, algorithm=ALGORITHM)


def hash_password(password: str) -> bytes:
    pw = bytes(password, "utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw, salt)


def check_password(password: str, password_in_db: bytes) -> bool:
    password_bytes = bytes(password, "utf-8")
    return bcrypt.checkpw(password_bytes, password_in_db)
