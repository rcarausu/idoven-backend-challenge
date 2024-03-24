from fastapi import APIRouter, Depends

from src.dependencies import register_ecg_service
from src.ecg.application.port.in_ports.models.ecg_model import ECGModel
from src.ecg.application.port.in_ports.register_ecg_use_case import RegisterEcgCommand
from src.ecg.application.service.register_ecg_service import RegisterEcgService

router = APIRouter(
    prefix="/ecg",
    tags=["ecg"]
)


@router.post("")
def save(ecg: ECGModel, service: RegisterEcgService = Depends(register_ecg_service)):
    ecg_id = service.register_ecg(RegisterEcgCommand(ecg))
    return ecg_id.value
