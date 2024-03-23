from typing import Optional

from ecg.application.port.out.load_ecg_port import LoadECGPort
from ecg.application.port.out.save_ecg_port import SaveECGPort
from ecg.domain.ecg import ECG, EcgId


class InMemoryECGPersistenceAdapter(LoadECGPort, SaveECGPort):

    def __init__(self):
        self.__ecg_repository = {}

    def load(self, ecg_id: EcgId) -> Optional[ECG]:
        # O(1) retrieval for average case or O(n) in worst case (hash collisions or too high load factor)
        return self.__ecg_repository.get(ecg_id.value, None)

    def save(self, ecg: ECG) -> EcgId:
        # O(1) insertion by using a dictionary
        self.__ecg_repository[ecg.id.value] = ecg
        return ecg.id
