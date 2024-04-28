from jose import jwt, JWTError
from fastapi import Depends
from src.exceptions import InvalidTokenException
from src.config import settings
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_data_from_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.JWT_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise InvalidTokenException
