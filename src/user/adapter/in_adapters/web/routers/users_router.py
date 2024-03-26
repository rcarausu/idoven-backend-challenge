from typing import Annotated

from fastapi import APIRouter, Header, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED

from src.dependencies import RegisterUserServiceDep
from src.user.adapter.in_adapters.web.models import RegisterUserInputModel, RegisterUserResponseModel
from src.user.application.port.in_ports.register_user_use_case import RegisterUserCommand, AdminToken
from src.user.application.port.in_ports.errors import InvalidAdminTokenError
from src.user.domain.user import User

router = APIRouter()


@router.post("", status_code=HTTP_201_CREATED)
def register_user(
        user_model: RegisterUserInputModel,
        x_admin_token: Annotated[str | None, Header()],
        service: RegisterUserServiceDep):
    try:
        user = User(user_model.username)
        service.register_user(RegisterUserCommand(AdminToken(x_admin_token), user))
        return RegisterUserResponseModel(username=user.username, token=user.token.value)
    except InvalidAdminTokenError as e:
        raise HTTPException(HTTP_401_UNAUTHORIZED, detail=e.message)
