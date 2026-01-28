"""
Kidney disease prediction schemas.
"""
from pydantic import BaseModel, Field
from typing import Literal
from app.api.schemas.common import PredictionResult


class KidneyDiseaseInput(BaseModel):
    """Input features for chronic kidney disease prediction."""
    
    age: float = Field(..., ge=1, le=120, description="Age in years")
    blood_pressure: float = Field(..., ge=40, le=200, description="Blood pressure (mm Hg)")
    specific_gravity: float = Field(..., ge=1.0, le=1.05, description="Urine specific gravity")
    albumin: float = Field(..., ge=0, le=5, description="Albumin level (0-5)")
    sugar: float = Field(..., ge=0, le=5, description="Sugar level (0-5)")
    red_blood_cells: Literal[0, 1] = Field(..., description="Red blood cells (0=Normal, 1=Abnormal)")
    pus_cell: Literal[0, 1] = Field(..., description="Pus cell (0=Normal, 1=Abnormal)")
    pus_cell_clumps: Literal[0, 1] = Field(..., description="Pus cell clumps (0=Not present, 1=Present)")
    bacteria: Literal[0, 1] = Field(..., description="Bacteria (0=Not present, 1=Present)")
    blood_glucose: float = Field(..., ge=20, le=500, description="Blood glucose random (mg/dL)")
    blood_urea: float = Field(..., ge=5, le=400, description="Blood urea (mg/dL)")
    serum_creatinine: float = Field(..., ge=0.1, le=20, description="Serum creatinine (mg/dL)")
    sodium: float = Field(..., ge=100, le=170, description="Sodium (mEq/L)")
    potassium: float = Field(..., ge=2, le=8, description="Potassium (mEq/L)")
    hemoglobin: float = Field(..., ge=3, le=20, description="Hemoglobin (g/dL)")
    packed_cell_volume: float = Field(..., ge=10, le=60, description="Packed cell volume (%)")
    white_blood_cell_count: float = Field(..., ge=2000, le=30000, description="WBC count")
    red_blood_cell_count: float = Field(..., ge=2, le=8, description="RBC count (millions/cmm)")
    
    def to_feature_dict(self) -> dict[str, float]:
        return {k: float(v) for k, v in self.model_dump().items()}


class KidneyPredictionResponse(BaseModel):
    result: PredictionResult
    input_summary: dict
    warnings: list[str] = []


def generate_warnings(input_data: KidneyDiseaseInput) -> list[str]:
    warnings = []
    if input_data.serum_creatinine > 1.2:
        warnings.append(f"Serum creatinine of {input_data.serum_creatinine} mg/dL is elevated")
    if input_data.blood_urea > 50:
        warnings.append(f"Blood urea of {input_data.blood_urea} mg/dL is high")
    if input_data.hemoglobin < 10:
        warnings.append(f"Hemoglobin of {input_data.hemoglobin} g/dL indicates anemia")
    return warnings
