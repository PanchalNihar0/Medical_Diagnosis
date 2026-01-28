"""
Common response schemas used across all disease endpoints.
"""
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class ConfidenceLevel(str, Enum):
    """Confidence level categories."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class FeatureContribution(BaseModel):
    """Single feature's contribution to prediction."""
    feature_name: str = Field(..., description="Name of the feature")
    display_name: str = Field(..., description="Human-readable feature name")
    value: float = Field(..., description="Input value for this feature")
    contribution: float = Field(..., description="SHAP contribution to prediction")
    interpretation: str = Field(..., description="Human-readable interpretation")


class PredictionResult(BaseModel):
    """Standardized prediction result."""
    disease: str = Field(..., description="Disease being predicted")
    prediction: int = Field(..., ge=0, le=1, description="0 = Low Risk, 1 = High Risk")
    probability: float = Field(..., ge=0.0, le=1.0, description="Probability of high risk")
    confidence_level: ConfidenceLevel = Field(..., description="Confidence category")
    
    # Explanations
    top_factors: list[FeatureContribution] = Field(
        default_factory=list,
        description="Top contributing factors to the prediction"
    )
    
    # Guidance
    recommendation: str = Field(..., description="Next steps recommendation")
    lifestyle_tips: list[str] = Field(
        default_factory=list,
        description="Evidence-based lifestyle recommendations"
    )
    
    # Comparison
    population_percentile: Optional[float] = Field(
        None,
        ge=0.0,
        le=100.0,
        description="Risk percentile compared to population"
    )
    
    # Disclaimers
    disclaimer: str = Field(
        default="This is a screening tool only. Results do not constitute medical diagnosis. "
                "Please consult a healthcare professional for proper evaluation.",
        description="Medical disclaimer"
    )


class WhatIfRequest(BaseModel):
    """Request for what-if analysis."""
    original_inputs: dict = Field(..., description="Original input values")
    modified_inputs: dict = Field(..., description="Modified input values to compare")


class WhatIfResponse(BaseModel):
    """Response for what-if analysis."""
    original_prediction: PredictionResult
    modified_prediction: PredictionResult
    probability_change: float = Field(..., description="Change in probability")
    key_changes: list[str] = Field(
        default_factory=list,
        description="Summary of what changed"
    )


class ReportRequest(BaseModel):
    """Request for PDF report generation."""
    prediction_result: PredictionResult
    patient_inputs: dict
    include_recommendations: bool = True
    include_explanations: bool = True


class ErrorResponse(BaseModel):
    """Standard error response."""
    error: str
    detail: Optional[str] = None
    field_errors: Optional[dict] = None
