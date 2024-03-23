from typing import Optional

from ecg.application.port.out.load_ecg_port import LoadEcgPort, LoadEcgQuery
from ecg.application.port.out.save_ecg_port import SaveEcgPort, SaveEcgCommand
from ecg.domain.ecg import ECG, EcgId


class InMemoryEcgPersistenceAdapter(LoadEcgPort, SaveEcgPort):

    def __init__(self):
        self.__ecg_repository = {}

    def load(self, query: LoadEcgQuery) -> Optional[ECG]:
        # O(1) retrieval for average case or O(n) in_adapters worst case (hash collisions or too high load factor)
        return self.__ecg_repository.get(query.ecg_id.value, None)

    def save(self, command: SaveEcgCommand) -> EcgId:
        # O(1) insertion by using a dictionary
        self.__ecg_repository[command.ecg.id.value] = command.ecg
        return command.ecg.id
