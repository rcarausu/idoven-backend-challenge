from typing import Annotated

from fastapi import Depends

from src.configuration import configuration
from src.ecg.adapter.out_adapters.persistence.in_memory_ecg_persistence_adapter import InMemoryEcgPersistenceAdapter
from src.ecg.application.service.register_ecg_service import RegisterEcgService
from src.insights.adapter.out_adapters.persistence.in_memory_insights_persistence_adapter import \
    InMemoryInsightsPersistenceAdapter
from src.insights.application.service.get_insights_service import GetInsightsService
from src.insights.application.service.process_insights_service import ProcessInsightsService
from src.user.adapter.out_adapters.in_memory_user_persistence_adapter import InMemoryUserPersistenceAdapter
from src.user.application.port.in_ports.register_user_use_case import AdminToken
from src.user.application.service.register_user_service import RegisterUserService

in_memory_ecg_repository = {}
in_memory_ecg_persistence_adapter = InMemoryEcgPersistenceAdapter(in_memory_ecg_repository)

in_memory_user_repository = {}
in_memory_user_persistence_adapter = InMemoryUserPersistenceAdapter(in_memory_user_repository)

in_memory_insights_repository = {}
in_memory_insights_persistence_adapter = InMemoryInsightsPersistenceAdapter(in_memory_insights_repository)


def register_ecg_service() -> RegisterEcgService:
    return RegisterEcgService(in_memory_ecg_persistence_adapter, in_memory_user_persistence_adapter, in_memory_insights_persistence_adapter)


RegisterEcgServiceDep = Annotated[register_ecg_service, Depends()]


def get_insights_service() -> GetInsightsService:
    return GetInsightsService(
        in_memory_ecg_persistence_adapter, in_memory_user_persistence_adapter, in_memory_insights_persistence_adapter
    )


GetInsightsServiceDep = Annotated[get_insights_service, Depends()]


def register_user_service() -> RegisterUserService:
    return RegisterUserService(in_memory_user_persistence_adapter, AdminToken(configuration().admin_token))


RegisterUserServiceDep = Annotated[register_user_service, Depends()]


def process_insights_service() -> ProcessInsightsService:
    return ProcessInsightsService(in_memory_insights_persistence_adapter)


ProcessInsightsServiceDep = Annotated[process_insights_service, Depends()]
