from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field


class UserSignupSchema(BaseModel):
    email: EmailStr = Field(...)
    firstname: str = Field(...)
    lastname: str = Field(...)
    telephone: str = Field(...)
    username: str = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Waynes Campbell",
                "email": "wayne@party.time",
                "password": "Excelent!",
            },
        }


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "wayne@party.time",
                "password": "Excelent!",
            },
        }
