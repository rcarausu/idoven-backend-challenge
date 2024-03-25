import json

from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND

from src.dependencies import RegisterEcgServiceDep, LoadEcgInsightsServiceDep
from src.ecg.adapter.in_adapters.web.models import (
    RegisterEsgInputModel,
    SaveEcgResponseModel, InsightsResponseModel, InsightResponseModel
)
from src.ecg.application.port.in_ports.load_ecg_insights_use_case import LoadEcgInsightsQuery
from src.ecg.application.port.in_ports.register_ecg_use_case import RegisterEcgCommand
from src.ecg.application.port.out_ports.get_ecg_port import EcgNotFoundError
from src.ecg.domain.ecg import EcgId

router = APIRouter()


@router.post("", status_code=HTTP_201_CREATED)
def register_ecg(ecg_model: RegisterEsgInputModel, service: RegisterEcgServiceDep):
    ecg_id = service.register_ecg(RegisterEcgCommand(ecg_model.as_ecg()))
    return SaveEcgResponseModel(id=ecg_id.value)


@router.get("/{ecg_id}/insights", status_code=HTTP_200_OK)
def load_ecg_insights(ecg_id: str, service: LoadEcgInsightsServiceDep):
    try:
        insights = service.get_insights(LoadEcgInsightsQuery(EcgId(ecg_id)))
        return InsightsResponseModel(
            leads=[InsightResponseModel(name=lead.name, number_of_zero_crossings=lead.number_of_zero_crossings)
                   for lead in insights.leads]
        )
    except EcgNotFoundError as e:
        return Response(
            content=json.dumps({"message": e.message}),
            status_code=HTTP_404_NOT_FOUND,
            media_type="application/json"
        )
