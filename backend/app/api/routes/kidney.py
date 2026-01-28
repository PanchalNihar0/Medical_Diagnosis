"""Kidney disease prediction endpoints."""
from fastapi import APIRouter, HTTPException
from app.config import logger
from app.api.schemas.kidney import KidneyDiseaseInput, KidneyPredictionResponse, generate_warnings
from app.api.schemas.common import WhatIfRequest, WhatIfResponse
from app.ml.inference import TabularInference

router = APIRouter()
kidney_inference = TabularInference(disease="kidney")


@router.post("/predict", response_model=KidneyPredictionResponse)
async def predict_kidney_disease(input_data: KidneyDiseaseInput) -> KidneyPredictionResponse:
    try:
        features = input_data.to_feature_dict()
        result = kidney_inference.predict(features)
        warnings = generate_warnings(input_data)
        input_summary = {"age": f"{input_data.age} years", "serum_creatinine": f"{input_data.serum_creatinine} mg/dL"}
        return KidneyPredictionResponse(result=result, input_summary=input_summary, warnings=warnings)
    except Exception as e:
        logger.error(f"Kidney prediction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/what-if", response_model=WhatIfResponse)
async def kidney_what_if(request: WhatIfRequest) -> WhatIfResponse:
    try:
        original = KidneyDiseaseInput(**request.original_inputs)
        modified = KidneyDiseaseInput(**request.modified_inputs)
        original_result = kidney_inference.predict(original.to_feature_dict())
        modified_result = kidney_inference.predict(modified.to_feature_dict())
        prob_change = modified_result.probability - original_result.probability
        key_changes = [f"{f}: {getattr(original, f)} → {getattr(modified, f)}" 
                       for f in original.model_fields if getattr(original, f) != getattr(modified, f)]
        return WhatIfResponse(original_prediction=original_result, modified_prediction=modified_result,
                             probability_change=prob_change, key_changes=key_changes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/info")
async def kidney_model_info() -> dict:
    try:
        return {"disease": "kidney", "model_version": kidney_inference.metadata.version}
    except Exception:
        return {"disease": "kidney", "status": "model_not_loaded"}
