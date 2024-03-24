from typing import List

from pydantic import BaseModel

from src.ecg.domain.ecg import ECG, Lead


class LeadModel(BaseModel):
    name: str
    number_of_samples: int | None = None
    signal: List[int]


class ECGModel(BaseModel):
    leads: list[LeadModel]


def as_ecg(ecg_model: ECGModel) -> ECG:
    leads = []
    for lead_model in ecg_model.leads:
        leads.append(
            Lead(
                lead_model.name,
                number_of_samples=lead_model.number_of_samples,
                signal=lead_model.signal
            ))
    return ECG(leads=leads)
