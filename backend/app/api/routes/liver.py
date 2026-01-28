"""Liver disease prediction endpoints."""
from fastapi import APIRouter, HTTPException
from app.config import logger
from app.api.schemas.liver import LiverDiseaseInput, LiverPredictionResponse, generate_warnings
from app.api.schemas.common import WhatIfRequest, WhatIfResponse
from app.ml.inference import TabularInference

router = APIRouter()
liver_inference = TabularInference(disease="liver")


@router.post("/predict", response_model=LiverPredictionResponse)
async def predict_liver_disease(input_data: LiverDiseaseInput) -> LiverPredictionResponse:
    try:
        result = liver_inference.predict(input_data.to_feature_dict())
        warnings = generate_warnings(input_data)
        return LiverPredictionResponse(result=result, input_summary=input_data.model_dump(), warnings=warnings)
    except Exception as e:
        logger.error(f"Liver prediction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/what-if", response_model=WhatIfResponse)
async def liver_what_if(request: WhatIfRequest) -> WhatIfResponse:
    try:
        original = LiverDiseaseInput(**request.original_inputs)
        modified = LiverDiseaseInput(**request.modified_inputs)
        orig_result = liver_inference.predict(original.to_feature_dict())
        mod_result = liver_inference.predict(modified.to_feature_dict())
        key_changes = [f"{f}: {getattr(original, f)} → {getattr(modified, f)}" 
                       for f in original.model_fields if getattr(original, f) != getattr(modified, f)]
        return WhatIfResponse(original_prediction=orig_result, modified_prediction=mod_result,
                             probability_change=mod_result.probability - orig_result.probability, key_changes=key_changes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/info")
async def liver_model_info() -> dict:
    try:
        return {"disease": "liver", "model_version": liver_inference.metadata.version}
    except Exception:
        return {"disease": "liver", "status": "model_not_loaded"}
