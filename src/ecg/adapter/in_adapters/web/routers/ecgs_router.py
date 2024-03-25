import json
from typing import Annotated

from fastapi import APIRouter, Response, Header
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED

from src.dependencies import RegisterEcgServiceDep, LoadEcgInsightsServiceDep
from src.ecg.adapter.in_adapters.web.models import (
    RegisterEsgInputModel,
    SaveEcgResponseModel, InsightsResponseModel, InsightResponseModel
)
from src.ecg.application.port.in_ports.load_ecg_insights_use_case import LoadEcgInsightsQuery
from src.ecg.application.port.in_ports.register_ecg_use_case import RegisterEcgCommand
from src.ecg.application.port.in_ports.errors import InvalidUserTokenError
from src.ecg.application.port.out_ports.get_ecg_port import EcgNotFoundError
from src.ecg.domain.ecg import EcgId, Lead
from src.ecg.domain.user import UserToken

router = APIRouter()


@router.post("", status_code=HTTP_201_CREATED)
def register_ecg(
        ecg_model: RegisterEsgInputModel,
        x_user_token: Annotated[str | None, Header()],
        register_ecg_service: RegisterEcgServiceDep
):
    user_token = UserToken(x_user_token)
    try:
        command = RegisterEcgCommand(
            user_token,
            [Lead(lead_model.name, lead_model.signal, lead_model.number_of_samples) for lead_model in ecg_model.leads]
        )
        ecg_id = register_ecg_service.register_ecg(command)
        return SaveEcgResponseModel(id=ecg_id.value)
    except InvalidUserTokenError as e:
        return Response(
            content=json.dumps({"message": e.message}),
            status_code=HTTP_401_UNAUTHORIZED,
            media_type="application/json"
        )


@router.get("/{ecg_id}/insights", status_code=HTTP_200_OK)
def load_ecg_insights(ecg_id: str, x_user_token: Annotated[str | None, Header()], service: LoadEcgInsightsServiceDep):
    try:
        insights = service.get_insights(LoadEcgInsightsQuery(EcgId(ecg_id), user_token=UserToken(x_user_token)))
        return InsightsResponseModel(
            leads=[InsightResponseModel(name=lead.name, number_of_zero_crossings=lead.number_of_zero_crossings)
                   for lead in insights.leads]
        )
    except InvalidUserTokenError as e:
        return Response(
            content=json.dumps({"message": e.message}),
            status_code=HTTP_401_UNAUTHORIZED,
            media_type="application/json"
        )
    except EcgNotFoundError as e:
        return Response(
            content=json.dumps({"message": e.message}),
            status_code=HTTP_404_NOT_FOUND,
            media_type="application/json"
        )
