"""
Report generation endpoint.
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from io import BytesIO

from app.config import logger
from app.api.schemas.common import ReportRequest
from app.services.report import get_report_generator


router = APIRouter()


@router.post("/generate")
async def generate_report(request: ReportRequest) -> StreamingResponse:
    """
    Generate a PDF report for a prediction result.
    
    Returns the PDF file as a downloadable stream.
    """
    try:
        generator = get_report_generator()
        
        pdf_bytes = generator.generate_report(
            prediction=request.prediction_result,
            patient_inputs=request.patient_inputs,
            include_recommendations=request.include_recommendations,
            include_explanations=request.include_explanations
        )
        
        # Create filename
        disease_name = request.prediction_result.disease.replace("_", "-")
        filename = f"health-assessment-{disease_name}.pdf"
        
        return StreamingResponse(
            BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
        
    except Exception as e:
        logger.error(f"Report generation failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate report: {str(e)}"
        )
