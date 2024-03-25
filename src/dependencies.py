from typing import Annotated

from fastapi import Depends

from src.ecg.application.service.load_ecg_insights_service import LoadEcgInsightsService
from src.ecg.adapter.out_adapters.persistence.in_memory_ecg_persistence_adapter import InMemoryEcgPersistenceAdapter
from src.ecg.application.service.register_ecg_service import RegisterEcgService

in_memory_ecg_persistence_adapter = InMemoryEcgPersistenceAdapter()


def register_ecg_service() -> RegisterEcgService:
    return RegisterEcgService(in_memory_ecg_persistence_adapter)


RegisterEcgServiceDep = Annotated[register_ecg_service, Depends()]


def load_ecg_insights_service() -> LoadEcgInsightsService:
    return LoadEcgInsightsService(in_memory_ecg_persistence_adapter)


LoadEcgInsightsServiceDep = Annotated[load_ecg_insights_service, Depends()]
