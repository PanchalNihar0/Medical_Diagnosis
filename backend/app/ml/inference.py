"""
ML Inference: Handles predictions with confidence scoring.
"""
import numpy as np
from typing import Any, Optional

from app.config import settings, logger
from app.api.schemas.common import ConfidenceLevel, PredictionResult, FeatureContribution
from app.ml.registry import get_registry, ModelMetadata


def get_confidence_level(probability: float) -> ConfidenceLevel:
    """
    Determine confidence level based on probability.
    
    Logic: Confidence is HIGH when probability is strongly toward 0 or 1.
    Confidence is LOW when probability is near 0.5 (uncertain).
    """
    distance_from_uncertain = abs(probability - 0.5)
    
    if distance_from_uncertain >= 0.3:  # prob <= 0.2 or prob >= 0.8
        return ConfidenceLevel.HIGH
    elif distance_from_uncertain >= 0.15:  # 0.2 < prob < 0.35 or 0.65 < prob < 0.8
        return ConfidenceLevel.MEDIUM
    else:  # 0.35 <= prob <= 0.65
        return ConfidenceLevel.LOW


def get_recommendation(prediction: int, confidence: ConfidenceLevel, disease: str) -> str:
    """Generate appropriate recommendation based on prediction and confidence."""
    
    if prediction == 0:  # Low risk
        if confidence == ConfidenceLevel.HIGH:
            return (
                f"Based on the provided data, your {disease} risk appears low. "
                "Continue maintaining a healthy lifestyle. Regular check-ups are still recommended."
            )
        else:
            return (
                f"Your {disease} risk appears low, but the model's confidence is limited. "
                "Consider discussing your risk factors with a healthcare provider."
            )
    else:  # High risk
        if confidence == ConfidenceLevel.HIGH:
            return (
                f"The analysis indicates elevated {disease} risk factors. "
                "We strongly recommend consulting a healthcare professional for proper evaluation and testing."
            )
        elif confidence == ConfidenceLevel.MEDIUM:
            return (
                f"Some {disease} risk factors were detected. "
                "Consider scheduling a check-up with your doctor to discuss these findings."
            )
        else:
            return (
                f"The results are inconclusive regarding {disease} risk. "
                "This screening cannot provide a clear assessment. Please consult a healthcare provider."
            )


class TabularInference:
    """
    Inference handler for tabular (sklearn) models.
    """
    
    def __init__(self, disease: str):
        self.disease = disease
        self.registry = get_registry()
        self._model = None
        self._metadata = None
        self._explainer = None
    
    @property
    def model(self) -> Any:
        """Lazy load model."""
        if self._model is None:
            self._model = self.registry.load_model(self.disease)
        return self._model
    
    @property
    def metadata(self) -> ModelMetadata:
        """Lazy load metadata."""
        if self._metadata is None:
            self._metadata = self.registry.get_metadata(self.disease)
        return self._metadata
    
    @property
    def explainer(self) -> Optional[Any]:
        """Lazy load SHAP explainer."""
        if self._explainer is None:
            self._explainer = self.registry.load_explainer(self.disease)
        return self._explainer
    
    def predict(self, features: dict[str, float]) -> PredictionResult:
        """
        Make a prediction with confidence and explanations.
        
        Args:
            features: Dictionary of feature name -> value
            
        Returns:
            Complete prediction result with explanations
        """
        # Convert features to array in correct order
        feature_order = self.metadata.features
        X = np.array([[features.get(f, 0.0) for f in feature_order]])
        
        # Get prediction and probability
        prediction = int(self.model.predict(X)[0])
        
        # Get probability (handle models without predict_proba)
        if hasattr(self.model, 'predict_proba'):
            probabilities = self.model.predict_proba(X)[0]
            probability = float(probabilities[1])  # Probability of positive class
        else:
            probability = float(prediction)  # Fallback for models without probability
        
        confidence_level = get_confidence_level(probability)
        recommendation = get_recommendation(prediction, confidence_level, self.disease)
        
        # Get SHAP explanations
        top_factors = self._get_shap_explanations(X, features)
        
        # Get lifestyle tips based on top risk factors
        lifestyle_tips = self._get_lifestyle_tips(top_factors, prediction)
        
        logger.info(
            f"Prediction for {self.disease}: {prediction} "
            f"(prob={probability:.3f}, confidence={confidence_level.value})"
        )
        
        return PredictionResult(
            disease=self.disease,
            prediction=prediction,
            probability=probability,
            confidence_level=confidence_level,
            top_factors=top_factors,
            recommendation=recommendation,
            lifestyle_tips=lifestyle_tips,
        )
    
    def _get_shap_explanations(
        self, 
        X: np.ndarray, 
        features: dict[str, float]
    ) -> list[FeatureContribution]:
        """Get SHAP-based feature contributions."""
        
        if self.explainer is None:
            logger.warning(f"No SHAP explainer available for {self.disease}")
            return []
        
        try:
            shap_values = self.explainer.shap_values(X)
            
            # Handle different SHAP output formats
            if isinstance(shap_values, list):
                # Binary classification: use positive class
                shap_vals = shap_values[1][0]
            else:
                shap_vals = shap_values[0]
            
            # Create contributions list
            contributions = []
            feature_names = self.metadata.feature_names
            
            for i, feat in enumerate(self.metadata.features):
                contribution = float(shap_vals[i])
                value = features.get(feat, 0.0)
                display_name = feature_names.get(feat, feat.replace("_", " ").title())
                
                # Generate interpretation
                if abs(contribution) < 0.01:
                    interpretation = f"{display_name} had minimal impact on the prediction"
                elif contribution > 0:
                    interpretation = f"{display_name} ({value:.1f}) increased risk assessment"
                else:
                    interpretation = f"{display_name} ({value:.1f}) decreased risk assessment"
                
                contributions.append(FeatureContribution(
                    feature_name=feat,
                    display_name=display_name,
                    value=value,
                    contribution=contribution,
                    interpretation=interpretation
                ))
            
            # Sort by absolute contribution and return top 5
            contributions.sort(key=lambda x: abs(x.contribution), reverse=True)
            return contributions[:5]
            
        except Exception as e:
            logger.error(f"Error computing SHAP values: {e}")
            return []
    
    def _get_lifestyle_tips(
        self, 
        top_factors: list[FeatureContribution],
        prediction: int
    ) -> list[str]:
        """Generate lifestyle recommendations based on risk factors."""
        
        # This is a simplified version - in production, you'd have a comprehensive
        # mapping of features to evidence-based recommendations
        tips = []
        
        if prediction == 0:
            tips.append("Continue your current healthy habits")
        
        for factor in top_factors[:3]:  # Top 3 factors
            if factor.contribution > 0.1:  # Positive contribution to risk
                if "glucose" in factor.feature_name.lower():
                    tips.append("Consider reducing sugar intake and increasing physical activity")
                elif "bmi" in factor.feature_name.lower() or "weight" in factor.feature_name.lower():
                    tips.append("Maintaining a healthy weight can significantly reduce health risks")
                elif "pressure" in factor.feature_name.lower() or "bp" in factor.feature_name.lower():
                    tips.append("Monitor blood pressure regularly and consider reducing sodium intake")
                elif "cholesterol" in factor.feature_name.lower():
                    tips.append("Focus on heart-healthy foods and regular cardiovascular exercise")
                elif "smoking" in factor.feature_name.lower():
                    tips.append("Smoking cessation is one of the most impactful health improvements")
                elif "alcohol" in factor.feature_name.lower():
                    tips.append("Moderate alcohol consumption can benefit overall health")
                elif "age" in factor.feature_name.lower():
                    tips.append("Regular health screenings become more important with age")
        
        if not tips:
            tips.append("Maintain a balanced diet and regular exercise routine")
            tips.append("Schedule regular check-ups with your healthcare provider")
        
        return tips[:4]  # Return max 4 tips
