"""
Model Registry: Handles loading, caching, and version management of ML models.
"""
import json
from pathlib import Path
from typing import Optional, Any
from functools import lru_cache

import joblib

# Try to import torch (optional, only needed for image models)
try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

from app.config import settings, logger


class ModelNotFoundError(Exception):
    """Raised when a model cannot be found."""
    pass


class ModelMetadata:
    """Metadata about a trained model."""
    
    def __init__(self, metadata_dict: dict):
        self.model_name = metadata_dict.get("model_name", "unknown")
        self.disease = metadata_dict.get("disease", "unknown")
        self.version = metadata_dict.get("version", "1.0")
        self.trained_at = metadata_dict.get("trained_at", "unknown")
        self.features = metadata_dict.get("features", [])
        self.feature_names = metadata_dict.get("feature_names", {})
        self.metrics = metadata_dict.get("metrics", {})
        self.clinical_ranges = metadata_dict.get("clinical_ranges", {})
        self.training_samples = metadata_dict.get("training_samples", 0)
        self.model_type = metadata_dict.get("model_type", "sklearn")


class ModelRegistry:
    """
    Central registry for loading and caching ML models.
    
    Each disease has its own directory under outputs/ with:
    - model.pkl or model.pt (the trained model)
    - metadata.json (training info, features, metrics)
    - shap_explainer.pkl (SHAP explainer for interpretability)
    """
    
    def __init__(self, models_dir: Optional[Path] = None):
        self.models_dir = models_dir or settings.models_dir
        self._models_cache: dict[str, Any] = {}
        self._metadata_cache: dict[str, ModelMetadata] = {}
        self._explainer_cache: dict[str, Any] = {}
        
    def _get_model_path(self, disease: str) -> Path:
        """Get the path to a disease's model directory."""
        return self.models_dir / disease
    
    def _load_metadata(self, disease: str) -> ModelMetadata:
        """Load model metadata from JSON file."""
        if disease in self._metadata_cache:
            return self._metadata_cache[disease]
            
        metadata_path = self._get_model_path(disease) / "metadata.json"
        
        if not metadata_path.exists():
            logger.warning(f"Metadata not found for {disease}, using defaults")
            return ModelMetadata({"disease": disease})
        
        with open(metadata_path, "r") as f:
            metadata_dict = json.load(f)
        
        metadata = ModelMetadata(metadata_dict)
        self._metadata_cache[disease] = metadata
        logger.info(f"Loaded metadata for {disease} model v{metadata.version}")
        
        return metadata
    
    def load_model(self, disease: str) -> Any:
        """
        Load a model for the specified disease.
        Models are cached after first load.
        
        Args:
            disease: Name of the disease (e.g., 'diabetes', 'heart')
            
        Returns:
            Loaded model object (sklearn or PyTorch)
            
        Raises:
            ModelNotFoundError: If model file doesn't exist
        """
        if disease in self._models_cache:
            return self._models_cache[disease]
        
        model_dir = self._get_model_path(disease)
        metadata = self._load_metadata(disease)
        
        # Try loading sklearn model first
        pkl_path = model_dir / "model.pkl"
        pt_path = model_dir / "model.pt"
        
        if pkl_path.exists():
            model = joblib.load(pkl_path)
            logger.info(f"Loaded sklearn model for {disease}")
        elif pt_path.exists() and TORCH_AVAILABLE:
            model = torch.load(pt_path, map_location=torch.device('cpu'))
            model.eval()
            logger.info(f"Loaded PyTorch model for {disease}")
        elif pt_path.exists() and not TORCH_AVAILABLE:
            raise ModelNotFoundError(
                f"PyTorch model exists for {disease} but torch is not installed"
            )
        else:
            raise ModelNotFoundError(
                f"No model found for {disease}. Expected at {pkl_path} or {pt_path}"
            )
        
        self._models_cache[disease] = model
        return model
    
    def load_explainer(self, disease: str) -> Optional[Any]:
        """
        Load SHAP explainer for a disease model.
        
        Args:
            disease: Name of the disease
            
        Returns:
            SHAP explainer object or None if not available
        """
        if disease in self._explainer_cache:
            return self._explainer_cache[disease]
        
        explainer_path = self._get_model_path(disease) / "shap_explainer.pkl"
        
        if not explainer_path.exists():
            logger.warning(f"SHAP explainer not found for {disease}")
            return None
        
        explainer = joblib.load(explainer_path)
        self._explainer_cache[disease] = explainer
        logger.info(f"Loaded SHAP explainer for {disease}")
        
        return explainer
    
    def get_metadata(self, disease: str) -> ModelMetadata:
        """Get metadata for a disease model."""
        return self._load_metadata(disease)
    
    def get_available_models(self) -> list[str]:
        """List all available disease models."""
        if not self.models_dir.exists():
            return []
        
        return [
            d.name for d in self.models_dir.iterdir()
            if d.is_dir() and (
                (d / "model.pkl").exists() or (d / "model.pt").exists()
            )
        ]
    
    def clear_cache(self):
        """Clear all cached models and metadata."""
        self._models_cache.clear()
        self._metadata_cache.clear()
        self._explainer_cache.clear()
        logger.info("Model cache cleared")


# Singleton instance
@lru_cache()
def get_registry() -> ModelRegistry:
    """Get the singleton model registry instance."""
    return ModelRegistry()
