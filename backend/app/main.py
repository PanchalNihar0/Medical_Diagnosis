"""
FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings, logger
from app.api.routes import health, diabetes, heart, kidney, liver, breast_cancer, malaria, pneumonia, report


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Industry-grade medical risk assessment API with ML-powered predictions",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Register routes
    app.include_router(health.router, prefix="/api/v1", tags=["Health"])
    app.include_router(diabetes.router, prefix="/api/v1/diabetes", tags=["Diabetes"])
    app.include_router(heart.router, prefix="/api/v1/heart", tags=["Heart Disease"])
    app.include_router(kidney.router, prefix="/api/v1/kidney", tags=["Kidney Disease"])
    app.include_router(liver.router, prefix="/api/v1/liver", tags=["Liver Disease"])
    app.include_router(breast_cancer.router, prefix="/api/v1/breast-cancer", tags=["Breast Cancer"])
    app.include_router(malaria.router, prefix="/api/v1/malaria", tags=["Malaria"])
    app.include_router(pneumonia.router, prefix="/api/v1/pneumonia", tags=["Pneumonia"])
    app.include_router(report.router, prefix="/api/v1/report", tags=["Reports"])
    
    logger.info(f"Application {settings.app_name} v{settings.app_version} initialized")
    
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.host, port=settings.port, reload=settings.debug)
