"""
Heart disease prediction schemas with clinical validation.
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
from app.api.schemas.common import PredictionResult


class HeartDiseaseInput(BaseModel):
    """Input features for heart disease risk prediction."""
    
    age: int = Field(..., ge=1, le=120, description="Age in years")
    sex: Literal[0, 1] = Field(..., description="Sex (0=Female, 1=Male)")
    chest_pain_type: Literal[0, 1, 2, 3] = Field(
        ..., 
        description="Chest pain type (0=Typical angina, 1=Atypical angina, 2=Non-anginal, 3=Asymptomatic)"
    )
    resting_bp: float = Field(..., ge=60, le=250, description="Resting blood pressure (mm Hg)")
    cholesterol: float = Field(..., ge=100, le=600, description="Serum cholesterol (mg/dL)")
    fasting_blood_sugar: Literal[0, 1] = Field(
        ..., 
        description="Fasting blood sugar > 120 mg/dL (0=No, 1=Yes)"
    )
    resting_ecg: Literal[0, 1, 2] = Field(
        ..., 
        description="Resting ECG results (0=Normal, 1=ST-T abnormality, 2=LV hypertrophy)"
    )
    max_heart_rate: float = Field(..., ge=60, le=220, description="Maximum heart rate achieved")
    exercise_angina: Literal[0, 1] = Field(
        ..., 
        description="Exercise induced angina (0=No, 1=Yes)"
    )
    st_depression: float = Field(..., ge=0, le=10, description="ST depression induced by exercise")
    st_slope: Literal[0, 1, 2] = Field(
        ..., 
        description="Slope of peak exercise ST segment (0=Upsloping, 1=Flat, 2=Downsloping)"
    )
    num_vessels: Literal[0, 1, 2, 3] = Field(
        ..., 
        description="Number of major vessels colored by fluoroscopy (0-3)"
    )
    thalassemia: Literal[1, 2, 3] = Field(
        ..., 
        description="Thalassemia (1=Normal, 2=Fixed defect, 3=Reversible defect)"
    )
    
    def to_feature_dict(self) -> dict[str, float]:
        return {k: float(v) for k, v in self.model_dump().items()}


class HeartPredictionResponse(BaseModel):
    result: PredictionResult
    input_summary: dict
    warnings: list[str] = []


def generate_warnings(input_data: HeartDiseaseInput) -> list[str]:
    warnings = []
    if input_data.cholesterol > 240:
        warnings.append(f"Cholesterol of {input_data.cholesterol} mg/dL is high")
    if input_data.resting_bp > 140:
        warnings.append(f"Blood pressure of {input_data.resting_bp} mm Hg is elevated")
    if input_data.max_heart_rate < 100:
        warnings.append("Low maximum heart rate may indicate reduced cardiac capacity")
    return warnings
