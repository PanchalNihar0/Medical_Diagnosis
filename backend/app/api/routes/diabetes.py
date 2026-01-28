"""
Diabetes prediction endpoints.
"""
from fastapi import APIRouter, HTTPException

from app.config import logger
from app.api.schemas.diabetes import (
    DiabetesInput,
    DiabetesPredictionResponse,
    generate_warnings
)
from app.api.schemas.common import PredictionResult, WhatIfRequest, WhatIfResponse
from app.ml.inference import TabularInference


router = APIRouter()


# Initialize inference engine
diabetes_inference = TabularInference(disease="diabetes")


@router.post("/predict", response_model=DiabetesPredictionResponse)
async def predict_diabetes(input_data: DiabetesInput) -> DiabetesPredictionResponse:
    """
    Predict diabetes risk based on clinical features.
    
    Returns a risk assessment with confidence level, contributing factors,
    and lifestyle recommendations.
    
    **Important**: This is a screening tool only and does not constitute
    a medical diagnosis.
    """
    try:
        # Convert input to feature dictionary
        features = input_data.to_feature_dict()
        
        # Make prediction
        result = diabetes_inference.predict(features)
        
        # Generate warnings for concerning input values
        warnings = generate_warnings(input_data)
        
        # Create input summary
        input_summary = {
            "pregnancies": input_data.pregnancies,
            "glucose": f"{input_data.glucose} mg/dL",
            "blood_pressure": f"{input_data.blood_pressure} mm Hg",
            "skin_thickness": f"{input_data.skin_thickness} mm",
            "insulin": f"{input_data.insulin} mu U/ml",
            "bmi": f"{input_data.bmi:.1f} kg/m²",
            "diabetes_pedigree": f"{input_data.diabetes_pedigree:.3f}",
            "age": f"{input_data.age} years"
        }
        
        logger.info(f"Diabetes prediction completed: risk={result.prediction}")
        
        return DiabetesPredictionResponse(
            result=result,
            input_summary=input_summary,
            warnings=warnings
        )
        
    except Exception as e:
        logger.error(f"Diabetes prediction failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


@router.post("/what-if", response_model=WhatIfResponse)
async def diabetes_what_if(request: WhatIfRequest) -> WhatIfResponse:
    """
    Compare predictions with modified input values.
    
    Allows users to see how changing certain values affects their risk.
    """
    try:
        # Validate both inputs
        original = DiabetesInput(**request.original_inputs)
        modified = DiabetesInput(**request.modified_inputs)
        
        # Get predictions
        original_result = diabetes_inference.predict(original.to_feature_dict())
        modified_result = diabetes_inference.predict(modified.to_feature_dict())
        
        # Calculate probability change
        prob_change = modified_result.probability - original_result.probability
        
        # Identify key changes
        key_changes = []
        for field in original.model_fields:
            orig_val = getattr(original, field)
            mod_val = getattr(modified, field)
            if orig_val != mod_val:
                key_changes.append(
                    f"{field.replace('_', ' ').title()}: {orig_val} → {mod_val}"
                )
        
        return WhatIfResponse(
            original_prediction=original_result,
            modified_prediction=modified_result,
            probability_change=prob_change,
            key_changes=key_changes
        )
        
    except Exception as e:
        logger.error(f"What-if analysis failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"What-if analysis failed: {str(e)}"
        )


@router.get("/info")
async def diabetes_model_info() -> dict:
    """
    Get information about the diabetes prediction model.
    """
    try:
        metadata = diabetes_inference.metadata
        return {
            "disease": "diabetes",
            "model_version": metadata.version,
            "trained_at": metadata.trained_at,
            "features": metadata.features,
            "feature_descriptions": metadata.feature_names,
            "metrics": metadata.metrics,
            "training_samples": metadata.training_samples
        }
    except Exception as e:
        logger.warning(f"Could not load model info: {e}")
        return {
            "disease": "diabetes",
            "status": "model_not_loaded",
            "message": "Model info will be available after training"
        }
