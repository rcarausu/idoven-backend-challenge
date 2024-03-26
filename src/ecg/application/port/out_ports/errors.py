from src.ecg.domain.ecg import EcgId


class EcgNotFoundError(Exception):
    def __init__(self, ecg_id: EcgId):
        self.message = f"ECG not found for id {ecg_id.value}"
        super().__init__(self.message)
