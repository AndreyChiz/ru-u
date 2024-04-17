from typing import Any

from fastapi import HTTPException, status


class RegUserBaseException(HTTPException):
    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL = "Something wrong"

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        super().__init__(status_code=self.STATUS_CODE, detail=self.DETAIL, **kwargs)


class UserAlreadyExistException(RegUserBaseException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "User with this email or login already exist"


class PaletteAlreadyExistException(RegUserBaseException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "You already hawe the palet with current name"


class UserCredantialsException(RegUserBaseException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Wrong password or user not exist"


class UserPasswordValidationException(RegUserBaseException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Password must contain at least one lower character, one upper character, digit or special symbol"


class PaletteNotFoundException(RegUserBaseException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = "Palette not found"


class InvalidTokenException(HTTPException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = "Invalid token"
    HEADERS = {"WWW-Authenticate": "Bearer"}

    def __init__(self):
        super().__init__(
            status_code=self.STATUS_CODE, detail=self.DETAIL, headers=self.HEADERS
        )


class ColorNameRequestException(RegUserBaseException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Can not get color name from HTTP"


class ColorAlreadyExistException(RegUserBaseException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "The color with the current name  is already exist in this palette"


class ColorNotExistExistException(RegUserBaseException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "The color with the current id is not exist in this palette"
