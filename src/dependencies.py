from src.ecg.adapter.out_adapters.persistence.in_memory_ecg_persistence_adapter import InMemoryEcgPersistenceAdapter
from src.ecg.application.service.register_ecg_service import RegisterEcgService


def register_ecg_service() -> RegisterEcgService:
    return RegisterEcgService(InMemoryEcgPersistenceAdapter())
