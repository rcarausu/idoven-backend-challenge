import json
from typing import Annotated

from fastapi import APIRouter, Header, HTTPException, BackgroundTasks, Response
from starlette.status import (
    HTTP_201_CREATED, HTTP_200_OK, HTTP_202_ACCEPTED, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED
)

from src.dependencies import RegisterEcgServiceDep, GetInsightsServiceDep, ProcessInsightsServiceDep
from src.ecg.adapter.in_adapters.web.models import (
    RegisterEsgInputModel,
    SaveEcgResponseModel, InsightsResponseModel, InsightResponseModel
)
from src.ecg.application.port.in_ports.register_ecg_use_case import RegisterEcgCommand
from src.ecg.application.port.out_ports.errors import EcgNotFoundError
from src.ecg.domain.ecg import EcgId, Lead
from src.insights.application.port.in_ports.errors import InsightsNotFoundError
from src.insights.application.port.in_ports.get_insights_use_case import GetInsightsQuery
from src.insights.application.port.out_ports.process_insights_use_case import ProcessInsightsCommand
from src.insights.domain.insights import InsightsStatus
from src.user.application.port.in_ports.errors import InvalidUserTokenError
from src.user.domain.user import UserToken

router = APIRouter()


@router.post("", status_code=HTTP_201_CREATED)
async def register_ecg(
        ecg_model: RegisterEsgInputModel,
        x_user_token: Annotated[str | None, Header()],
        register_ecg_service: RegisterEcgServiceDep,
        process_insights_service: ProcessInsightsServiceDep,
        background_tasks: BackgroundTasks
):
    user_token = UserToken(x_user_token)
    try:
        leads = [
            Lead(lead_model.name, lead_model.signal, lead_model.number_of_samples)
            for lead_model in ecg_model.leads
        ]
        ecg_id = register_ecg_service.register_ecg(RegisterEcgCommand(user_token, leads))
        background_tasks.add_task(process_insights_service.process_insights, ProcessInsightsCommand(ecg_id, leads))
        return SaveEcgResponseModel(id=ecg_id.value)
    except InvalidUserTokenError as e:
        raise HTTPException(HTTP_401_UNAUTHORIZED, detail=e.message)


@router.get("/{ecg_id}/insights", status_code=HTTP_200_OK)
def load_ecg_insights(ecg_id: str, x_user_token: Annotated[str | None, Header()], service: GetInsightsServiceDep):
    try:
        insights = service.get_insights(GetInsightsQuery(EcgId(ecg_id), user_token=UserToken(x_user_token)))
        if insights.status == InsightsStatus.IN_PROGRESS:
            return Response(
                status_code=HTTP_202_ACCEPTED,
                media_type="application/json",
                content=json.dumps({"detail": "Insights are still being processed"})
            )

        return InsightsResponseModel(
            ecg_id=insights.ecg_id.value,
            leads=[InsightResponseModel(name=lead.name, number_of_zero_crossings=lead.number_of_zero_crossings)
                   for lead in insights.leads]
        )
    except InvalidUserTokenError as e:
        raise HTTPException(HTTP_401_UNAUTHORIZED, detail=e.message)
    except EcgNotFoundError as e:
        raise HTTPException(HTTP_404_NOT_FOUND, detail=e.message)
    except InsightsNotFoundError as e:
        raise HTTPException(HTTP_404_NOT_FOUND, detail=e.message)
