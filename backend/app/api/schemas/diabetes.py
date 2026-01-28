"""
Diabetes prediction schemas with clinical validation.
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional

from app.api.schemas.common import PredictionResult


class DiabetesInput(BaseModel):
    """
    Input features for diabetes risk prediction.
    
    Based on the Pima Indians Diabetes Dataset features,
    with clinical range validation.
    """
    
    pregnancies: int = Field(
        ...,
        ge=0,
        le=20,
        description="Number of pregnancies (0-20)",
        json_schema_extra={"example": 2}
    )
    
    glucose: float = Field(
        ...,
        gt=0,
        le=300,
        description="Plasma glucose concentration (mg/dL) from 2-hour oral glucose tolerance test",
        json_schema_extra={"example": 120}
    )
    
    blood_pressure: float = Field(
        ...,
        ge=0,
        le=200,
        description="Diastolic blood pressure (mm Hg)",
        json_schema_extra={"example": 72}
    )
    
    skin_thickness: float = Field(
        ...,
        ge=0,
        le=100,
        description="Triceps skin fold thickness (mm)",
        json_schema_extra={"example": 23}
    )
    
    insulin: float = Field(
        ...,
        ge=0,
        le=1000,
        description="2-Hour serum insulin (mu U/ml)",
        json_schema_extra={"example": 85}
    )
    
    bmi: float = Field(
        ...,
        gt=0,
        le=70,
        description="Body mass index (kg/m²)",
        json_schema_extra={"example": 28.5}
    )
    
    diabetes_pedigree: float = Field(
        ...,
        ge=0,
        le=3,
        description="Diabetes pedigree function (genetic risk score)",
        json_schema_extra={"example": 0.52}
    )
    
    age: int = Field(
        ...,
        ge=1,
        le=120,
        description="Age in years",
        json_schema_extra={"example": 45}
    )
    
    @field_validator('glucose')
    @classmethod
    def validate_glucose(cls, v: float) -> float:
        if v == 0:
            raise ValueError("Glucose cannot be 0 - this indicates missing data")
        return v
    
    @field_validator('blood_pressure')
    @classmethod
    def validate_blood_pressure(cls, v: float) -> float:
        if v == 0:
            # Allow 0 but flag it - some datasets use 0 for missing
            pass
        return v
    
    @field_validator('bmi')
    @classmethod
    def validate_bmi(cls, v: float) -> float:
        if v < 10:
            raise ValueError("BMI below 10 is not physiologically possible")
        return v
    
    def to_feature_dict(self) -> dict[str, float]:
        """Convert to feature dictionary for model input."""
        return {
            "pregnancies": float(self.pregnancies),
            "glucose": self.glucose,
            "blood_pressure": self.blood_pressure,
            "skin_thickness": self.skin_thickness,
            "insulin": self.insulin,
            "bmi": self.bmi,
            "diabetes_pedigree": self.diabetes_pedigree,
            "age": float(self.age)
        }


class DiabetesPredictionResponse(BaseModel):
    """Response for diabetes prediction."""
    
    result: PredictionResult
    input_summary: dict = Field(..., description="Summary of input values")
    
    # Field-specific warnings
    warnings: list[str] = Field(
        default_factory=list,
        description="Warnings about input values outside normal ranges"
    )


# Clinical reference ranges for generating warnings
CLINICAL_RANGES = {
    "glucose": {
        "normal": (70, 99),
        "prediabetes": (100, 125),
        "diabetes": (126, float('inf')),
        "unit": "mg/dL"
    },
    "blood_pressure": {
        "normal": (60, 80),
        "elevated": (80, 89),
        "high": (90, float('inf')),
        "unit": "mm Hg"
    },
    "bmi": {
        "underweight": (0, 18.5),
        "normal": (18.5, 25),
        "overweight": (25, 30),
        "obese": (30, float('inf')),
        "unit": "kg/m²"
    }
}


def generate_warnings(input_data: DiabetesInput) -> list[str]:
    """Generate clinical warnings for input values."""
    warnings = []
    
    # Glucose warnings
    if input_data.glucose >= 126:
        warnings.append(
            f"Fasting glucose of {input_data.glucose} mg/dL is in the diabetic range. "
            "Consult a doctor for proper testing."
        )
    elif input_data.glucose >= 100:
        warnings.append(
            f"Glucose of {input_data.glucose} mg/dL indicates prediabetes range."
        )
    
    # BMI warnings
    if input_data.bmi >= 30:
        warnings.append(
            f"BMI of {input_data.bmi:.1f} kg/m² is in the obese category."
        )
    elif input_data.bmi >= 25:
        warnings.append(
            f"BMI of {input_data.bmi:.1f} kg/m² is in the overweight category."
        )
    
    # Blood pressure
    if input_data.blood_pressure >= 90:
        warnings.append(
            f"Diastolic blood pressure of {input_data.blood_pressure} mm Hg is elevated."
        )
    
    return warnings
