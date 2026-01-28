"""Liver disease prediction schemas."""
from pydantic import BaseModel, Field
from typing import Literal
from app.api.schemas.common import PredictionResult


class LiverDiseaseInput(BaseModel):
    age: int = Field(..., ge=1, le=120)
    gender: Literal[0, 1] = Field(..., description="0=Female, 1=Male")
    total_bilirubin: float = Field(..., ge=0, le=100)
    direct_bilirubin: float = Field(..., ge=0, le=50)
    alkaline_phosphatase: float = Field(..., ge=40, le=3000)
    alamine_aminotransferase: float = Field(..., ge=5, le=3000)
    aspartate_aminotransferase: float = Field(..., ge=5, le=5000)
    total_proteins: float = Field(..., ge=2, le=12)
    albumin: float = Field(..., ge=0.5, le=6)
    albumin_globulin_ratio: float = Field(..., ge=0.1, le=3)
    
    def to_feature_dict(self) -> dict[str, float]:
        return {k: float(v) for k, v in self.model_dump().items()}


class LiverPredictionResponse(BaseModel):
    result: PredictionResult
    input_summary: dict
    warnings: list[str] = []


def generate_warnings(input_data: LiverDiseaseInput) -> list[str]:
    warnings = []
    if input_data.total_bilirubin > 1.2:
        warnings.append(f"Total bilirubin of {input_data.total_bilirubin} is elevated")
    if input_data.alamine_aminotransferase > 40:
        warnings.append(f"ALT of {input_data.alamine_aminotransferase} U/L is elevated")
    return warnings
