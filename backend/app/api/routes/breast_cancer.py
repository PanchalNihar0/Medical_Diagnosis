"""Breast cancer prediction endpoints."""
from fastapi import APIRouter, HTTPException
from app.config import logger
from app.api.schemas.breast_cancer import BreastCancerInput, BreastCancerPredictionResponse
from app.ml.inference import TabularInference

router = APIRouter()
breast_cancer_inference = TabularInference(disease="breast_cancer")


@router.post("/predict", response_model=BreastCancerPredictionResponse)
async def predict_breast_cancer(input_data: BreastCancerInput) -> BreastCancerPredictionResponse:
    try:
        result = breast_cancer_inference.predict(input_data.to_feature_dict())
        return BreastCancerPredictionResponse(result=result, input_summary=input_data.model_dump(), warnings=[])
    except Exception as e:
        logger.error(f"Breast cancer prediction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/info")
async def breast_cancer_model_info() -> dict:
    try:
        return {"disease": "breast_cancer", "model_version": breast_cancer_inference.metadata.version}
    except Exception:
        return {"disease": "breast_cancer", "status": "model_not_loaded"}
