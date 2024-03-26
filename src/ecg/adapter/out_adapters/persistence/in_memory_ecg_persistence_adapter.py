from typing import Optional

from src.ecg.application.port.out_ports.get_ecg_port import GetEcgPort
from src.ecg.application.port.out_ports.save_ecg_port import SaveEcgPort
from src.ecg.domain.ecg import ECG, EcgId


class InMemoryEcgPersistenceAdapter(GetEcgPort, SaveEcgPort):

    def __init__(self, repository: dict):
        self.__repository = repository

    def get(self, ecg_id: EcgId) -> Optional[ECG]:
        # O(1) retrieval for average case or O(n) in_adapters worst case (hash collisions or too high load factor)
        return self.__repository.get(ecg_id.value, None)

    def save(self, ecg: ECG) -> EcgId:
        # O(1) insertion by using a dictionary
        self.__repository[ecg.id.value] = ecg
        return ecg.id
