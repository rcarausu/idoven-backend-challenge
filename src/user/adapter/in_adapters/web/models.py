from pydantic import BaseModel


class RegisterUserInputModel(BaseModel):
    username: str


class RegisterUserResponseModel(BaseModel):
    username: str
    token: str
