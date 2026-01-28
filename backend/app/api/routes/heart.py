"""
Heart disease prediction endpoints.
"""
from fastapi import APIRouter, HTTPException
from app.config import logger
from app.api.schemas.heart import HeartDiseaseInput, HeartPredictionResponse, generate_warnings
from app.api.schemas.common import WhatIfRequest, WhatIfResponse
from app.ml.inference import TabularInference

router = APIRouter()
heart_inference = TabularInference(disease="heart")


@router.post("/predict", response_model=HeartPredictionResponse)
async def predict_heart_disease(input_data: HeartDiseaseInput) -> HeartPredictionResponse:
    """Predict heart disease risk based on clinical features."""
    try:
        features = input_data.to_feature_dict()
        result = heart_inference.predict(features)
        warnings = generate_warnings(input_data)
        
        input_summary = {
            "age": f"{input_data.age} years",
            "sex": "Male" if input_data.sex == 1 else "Female",
            "resting_bp": f"{input_data.resting_bp} mm Hg",
            "cholesterol": f"{input_data.cholesterol} mg/dL",
            "max_heart_rate": f"{input_data.max_heart_rate} bpm"
        }
        
        return HeartPredictionResponse(result=result, input_summary=input_summary, warnings=warnings)
    except Exception as e:
        logger.error(f"Heart prediction failed: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@router.post("/what-if", response_model=WhatIfResponse)
async def heart_what_if(request: WhatIfRequest) -> WhatIfResponse:
    """Compare predictions with modified input values."""
    try:
        original = HeartDiseaseInput(**request.original_inputs)
        modified = HeartDiseaseInput(**request.modified_inputs)
        original_result = heart_inference.predict(original.to_feature_dict())
        modified_result = heart_inference.predict(modified.to_feature_dict())
        prob_change = modified_result.probability - original_result.probability
        
        key_changes = []
        for field in original.model_fields:
            if getattr(original, field) != getattr(modified, field):
                key_changes.append(f"{field}: {getattr(original, field)} → {getattr(modified, field)}")
        
        return WhatIfResponse(
            original_prediction=original_result,
            modified_prediction=modified_result,
            probability_change=prob_change,
            key_changes=key_changes
        )
    except Exception as e:
        logger.error(f"Heart what-if failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/info")
async def heart_model_info() -> dict:
    try:
        metadata = heart_inference.metadata
        return {"disease": "heart", "model_version": metadata.version, "features": metadata.features}
    except Exception:
        return {"disease": "heart", "status": "model_not_loaded"}
