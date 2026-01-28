"""Breast cancer prediction schemas."""
from pydantic import BaseModel, Field
from app.api.schemas.common import PredictionResult


class BreastCancerInput(BaseModel):
    """Input features for breast cancer prediction (Wisconsin Diagnostic dataset)."""
    
    # Mean features
    radius_mean: float = Field(..., ge=0)
    texture_mean: float = Field(..., ge=0)
    perimeter_mean: float = Field(..., ge=0)
    area_mean: float = Field(..., ge=0)
    smoothness_mean: float = Field(..., ge=0)
    compactness_mean: float = Field(..., ge=0)
    concavity_mean: float = Field(..., ge=0)
    concave_points_mean: float = Field(..., ge=0)
    symmetry_mean: float = Field(..., ge=0)
    fractal_dimension_mean: float = Field(..., ge=0)
    
    # SE features
    radius_se: float = Field(..., ge=0)
    texture_se: float = Field(..., ge=0)
    perimeter_se: float = Field(..., ge=0)
    area_se: float = Field(..., ge=0)
    smoothness_se: float = Field(..., ge=0)
    compactness_se: float = Field(..., ge=0)
    concavity_se: float = Field(..., ge=0)
    concave_points_se: float = Field(..., ge=0)
    symmetry_se: float = Field(..., ge=0)
    fractal_dimension_se: float = Field(..., ge=0)
    
    # Worst features
    radius_worst: float = Field(..., ge=0)
    texture_worst: float = Field(..., ge=0)
    perimeter_worst: float = Field(..., ge=0)
    area_worst: float = Field(..., ge=0)
    smoothness_worst: float = Field(..., ge=0)
    compactness_worst: float = Field(..., ge=0)
    
    def to_feature_dict(self) -> dict[str, float]:
        return {k: float(v) for k, v in self.model_dump().items()}


class BreastCancerPredictionResponse(BaseModel):
    result: PredictionResult
    input_summary: dict
    warnings: list[str] = []
