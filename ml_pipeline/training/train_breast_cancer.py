"""
Breast Cancer Model Training Pipeline.
Uses Wisconsin Diagnostic Breast Cancer dataset from sklearn.
"""
import json
import warnings
from datetime import datetime
from pathlib import Path

import joblib
import numpy as np
import shap
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, recall_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.calibration import CalibratedClassifierCV

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import OUTPUTS_DIR, RANDOM_STATE, TEST_SIZE, CV_FOLDS

warnings.filterwarnings('ignore')


def train_and_evaluate():
    """Main training pipeline."""
    print("=" * 60)
    print("BREAST CANCER MODEL TRAINING PIPELINE")
    print("=" * 60)
    
    # Load from sklearn
    data = load_breast_cancer()
    X = data.data
    y = data.target
    feature_cols = list(data.feature_names)
    
    print(f"Loaded {len(X)} samples, {len(feature_cols)} features")
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )
    
    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=RANDOM_STATE, class_weight='balanced')
    
    cv = StratifiedKFold(n_splits=CV_FOLDS, shuffle=True, random_state=RANDOM_STATE)
    cv_scores = cross_val_score(model, X_train, y_train, cv=cv, scoring='roc_auc')
    print(f"CV AUC: {cv_scores.mean():.4f}")
    
    model.fit(X_train, y_train)
    calibrated = CalibratedClassifierCV(model, cv=3, method='sigmoid')
    calibrated.fit(X_train, y_train)
    
    y_pred = calibrated.predict(X_test)
    y_proba = calibrated.predict_proba(X_test)[:, 1]
    
    metrics = {
        'accuracy': float(accuracy_score(y_test, y_pred)),
        'recall': float(recall_score(y_test, y_pred)),
        'roc_auc': float(roc_auc_score(y_test, y_proba)),
    }
    print(f"Accuracy: {metrics['accuracy']:.4f}, Recall: {metrics['recall']:.4f}, AUC: {metrics['roc_auc']:.4f}")
    
    explainer = shap.TreeExplainer(model)
    
    output_dir = OUTPUTS_DIR / "breast_cancer"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    joblib.dump(calibrated, output_dir / "model.pkl")
    joblib.dump(explainer, output_dir / "shap_explainer.pkl")
    
    metadata = {
        "model_name": "RandomForest", "disease": "breast_cancer", "version": "2.0.0",
        "trained_at": datetime.now().isoformat(), "features": feature_cols,
        "metrics": metrics, "training_samples": len(X_train), "model_type": "sklearn",
    }
    with open(output_dir / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    
    print(f"✓ Saved to {output_dir}")


if __name__ == "__main__":
    train_and_evaluate()
