from fastapi import APIRouter, Depends
from pydantic import BaseModel
from starlette.status import HTTP_201_CREATED

from src.dependencies import register_ecg_service
from src.ecg.application.port.in_ports.models.ecg_model import ECGModel
from src.ecg.application.port.in_ports.register_ecg_use_case import RegisterEcgCommand
from src.ecg.application.service.register_ecg_service import RegisterEcgService

router = APIRouter(
    prefix="/ecg",
    tags=["ecg"]
)


class SaveEcgResponseModel(BaseModel):
    id: str


@router.post("", status_code=HTTP_201_CREATED)
def save(ecg: ECGModel, service: RegisterEcgService = Depends(register_ecg_service)):
    ecg_id = service.register_ecg(RegisterEcgCommand(ecg))
    return SaveEcgResponseModel(id=ecg_id.value)
