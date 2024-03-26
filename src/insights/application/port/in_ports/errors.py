from src.ecg.domain.ecg import EcgId


class InsightsNotFoundError(Exception):

    def __init__(self, ecg_id: EcgId):
        self.message = f"No insights found for ecg {ecg_id}"
        super().__init__(self.message)
