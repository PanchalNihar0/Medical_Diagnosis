"""
Diabetes Model Training Pipeline - Fixed version.
"""
import json
import warnings
from datetime import datetime
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import shap
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import OUTPUTS_DIR, RAW_DATA_DIR, FEATURE_NAMES, RANDOM_STATE, TEST_SIZE, CV_FOLDS

warnings.filterwarnings('ignore')


def load_and_prepare_data():
    """Load Pima Indians Diabetes dataset."""
    data_path = RAW_DATA_DIR / "diabetes.csv"
    
    if not data_path.exists():
        print("Downloading Pima Indians Diabetes dataset...")
        url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
        columns = ['pregnancies', 'glucose', 'blood_pressure', 'skin_thickness',
                   'insulin', 'bmi', 'diabetes_pedigree', 'age', 'target']
        df = pd.read_csv(url, names=columns)
        RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
        df.to_csv(data_path, index=False)
        print(f"Saved to {data_path}")
    else:
        df = pd.read_csv(data_path)
        if 'target' not in df.columns:
            columns = ['pregnancies', 'glucose', 'blood_pressure', 'skin_thickness',
                       'insulin', 'bmi', 'diabetes_pedigree', 'age', 'target']
            df = pd.read_csv(data_path, names=columns)
    
    print(f"Loaded {len(df)} samples")
    return df


def handle_missing_values(df):
    """Replace 0s with medians for physiological columns."""
    df = df.copy()
    zero_invalid = ['glucose', 'blood_pressure', 'skin_thickness', 'insulin', 'bmi']
    for col in zero_invalid:
        if col in df.columns:
            df[col] = df[col].replace(0, np.nan)
            df[col] = df[col].fillna(df[col].median())
    return df


def train_and_evaluate():
    """Main training pipeline."""
    print("=" * 60)
    print("DIABETES MODEL TRAINING PIPELINE")
    print("=" * 60)
    
    df = load_and_prepare_data()
    df = handle_missing_values(df)
    
    feature_cols = ['pregnancies', 'glucose', 'blood_pressure', 'skin_thickness',
                    'insulin', 'bmi', 'diabetes_pedigree', 'age']
    
    X = df[feature_cols]
    y = df['target']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )
    print(f"Training: {len(X_train)}, Test: {len(X_test)}")
    
    # Use RandomForest - doesn't need scaling and pickles easily
    model = RandomForestClassifier(
        n_estimators=100, max_depth=10, random_state=RANDOM_STATE, class_weight='balanced'
    )
    
    cv = StratifiedKFold(n_splits=CV_FOLDS, shuffle=True, random_state=RANDOM_STATE)
    cv_scores = cross_val_score(model, X_train, y_train, cv=cv, scoring='roc_auc')
    print(f"CV AUC: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
    
    model.fit(X_train, y_train)
    
    # Evaluate before calibration
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    
    metrics = {
        'accuracy': float(accuracy_score(y_test, y_pred)),
        'precision': float(precision_score(y_test, y_pred)),
        'recall': float(recall_score(y_test, y_pred)),
        'f1': float(f1_score(y_test, y_pred)),
        'roc_auc': float(roc_auc_score(y_test, y_proba)),
    }
    
    print(f"Accuracy: {metrics['accuracy']:.4f}")
    print(f"Recall: {metrics['recall']:.4f}")
    print(f"ROC-AUC: {metrics['roc_auc']:.4f}")
    
    # Create SHAP explainer
    explainer = shap.TreeExplainer(model)
    
    # Save
    output_dir = OUTPUTS_DIR / "diabetes"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    joblib.dump(model, output_dir / "model.pkl")
    print(f"✓ Model saved")
    
    joblib.dump(explainer, output_dir / "shap_explainer.pkl")
    print(f"✓ SHAP explainer saved")
    
    metadata = {
        "model_name": "RandomForest",
        "disease": "diabetes",
        "version": "2.0.0",
        "trained_at": datetime.now().isoformat(),
        "features": feature_cols,
        "feature_names": FEATURE_NAMES.get("diabetes", {}),
        "metrics": metrics,
        "training_samples": len(X_train),
        "model_type": "sklearn",
    }
    
    with open(output_dir / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"✓ Metadata saved to {output_dir}")
    
    print("\n" + "=" * 60)
    print("TRAINING COMPLETE")
    print("=" * 60)
    
    return model, metadata


if __name__ == "__main__":
    train_and_evaluate()
