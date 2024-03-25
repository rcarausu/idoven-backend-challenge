from typing import List

from pydantic import BaseModel

from src.ecg.domain.ecg import ECG, Lead


class LeadInputModel(BaseModel):
    name: str
    number_of_samples: int | None = None
    signal: List[int]


class RegisterEsgInputModel(BaseModel):
    leads: list[LeadInputModel]

    def as_ecg(self) -> ECG:
        leads = []
        for lead_model in self.leads:
            leads.append(
                Lead(
                    lead_model.name,
                    number_of_samples=lead_model.number_of_samples,
                    signal=lead_model.signal
                ))
        return ECG(leads=leads)


class RegisterUserInputModel(BaseModel):
    username: str


class RegisterUserResponseModel(BaseModel):
    username: str
    token: str


class SaveEcgResponseModel(BaseModel):
    id: str


class InsightResponseModel(BaseModel):
    name: str
    number_of_zero_crossings: int


class InsightsResponseModel(BaseModel):
    leads: List[InsightResponseModel]
