"""
Application configuration.
Compatible with Pydantic v1 and v2.
"""
from pathlib import Path
from typing import List
import logging
import os


class Settings:
    """Application settings with defaults."""
    
    def __init__(self):
        # API settings
        self.app_name: str = os.getenv("APP_NAME", "Medical Diagnosis API")
        self.app_version: str = "2.0.0"
        self.debug: bool = os.getenv("DEBUG", "false").lower() == "true"
        
        # Server settings
        self.host: str = os.getenv("HOST", "0.0.0.0")
        self.port: int = int(os.getenv("PORT", "8000"))
        
        # CORS settings
        cors_origins_env = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000")
        self.cors_origins: List[str] = [o.strip() for o in cors_origins_env.split(",")]
        
        # Model settings
        self.models_dir: Path = Path(__file__).parent.parent.parent / "ml_pipeline" / "outputs"
        
        # Confidence thresholds
        self.confidence_low_threshold: float = 0.4
        self.confidence_high_threshold: float = 0.7
        
        # Logging
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()


def setup_logging() -> logging.Logger:
    """Configure application logging."""
    logging.basicConfig(
        level=getattr(logging, settings.log_level),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    return logging.getLogger("medical_diagnosis")


logger = setup_logging()
