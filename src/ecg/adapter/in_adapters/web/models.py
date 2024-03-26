from typing import List

from pydantic import BaseModel


class LeadInputModel(BaseModel):
    name: str
    number_of_samples: int | None = None
    signal: List[int]


class RegisterEsgInputModel(BaseModel):
    leads: list[LeadInputModel]


class SaveEcgResponseModel(BaseModel):
    id: str


class InsightResponseModel(BaseModel):
    name: str
    number_of_zero_crossings: int


class InsightsResponseModel(BaseModel):
    leads: List[InsightResponseModel]
