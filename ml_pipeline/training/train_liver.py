"""
Liver Disease Model Training - Real Indian Liver Patient Dataset (UCI).
"""
import json
import warnings
from datetime import datetime
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import shap
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, recall_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import OUTPUTS_DIR, RAW_DATA_DIR, RANDOM_STATE, TEST_SIZE, CV_FOLDS

warnings.filterwarnings('ignore')

# Standard column names for ILPD dataset
COLUMNS = [
    'age', 'gender', 'total_bilirubin', 'direct_bilirubin',
    'alkaline_phosphatase', 'alamine_aminotransferase',
    'aspartate_aminotransferase', 'total_proteins',
    'albumin', 'albumin_globulin_ratio', 'target'
]


def load_and_prepare_data():
    """Load Indian Liver Patient Dataset."""
    data_path = RAW_DATA_DIR / "liver.csv"
    
    if not data_path.exists():
        print("Downloading Indian Liver Patient Dataset...")
        
        # Verified working URLs
        urls = [
            "https://raw.githubusercontent.com/mikeizbicki/datasets/master/csv/uci/Indian%20Liver%20Patient%20Dataset%20(ILPD).csv",
            "https://raw.githubusercontent.com/mchifala/liver-disease-classification/master/Indian%20Liver%20Patient%20Dataset%20(ILPD).csv",
        ]
        
        df = None
        for url in urls:
            try:
                print(f"Trying: {url}")
                # This dataset has no header, so specify column names
                df = pd.read_csv(url, names=COLUMNS, header=None)
                print(f"✓ Downloaded {len(df)} samples!")
                break
            except Exception as e:
                print(f"✗ Failed: {e}")
                continue
        
        if df is None:
            raise RuntimeError("Could not download liver disease dataset")
        
        RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
        df.to_csv(data_path, index=False)
        print(f"Saved to {data_path}")
    else:
        # Try to read existing file - check if it has header
        df = pd.read_csv(data_path)
        if 'target' not in df.columns:
            # No header, re-read with column names
            df = pd.read_csv(data_path, names=COLUMNS, header=None)
    
    return prepare_liver_data(df)


def prepare_liver_data(df):
    """Clean and prepare the liver dataset."""
    # Handle gender
    df['gender'] = df['gender'].map({'Male': 1, 'Female': 0, 'male': 1, 'female': 0})
    df['gender'] = df['gender'].fillna(1).astype(float)
    
    # Handle target: 1 = liver patient, 2 = healthy -> 1 = disease, 0 = healthy
    df['target'] = df['target'].apply(lambda x: 1 if x == 1 else 0)
    
    # Drop rows with missing values
    df = df.dropna()
    
    # Get feature columns (all except target)
    feature_cols = [c for c in df.columns if c != 'target']
    
    print(f"Loaded {len(df)} samples with {len(feature_cols)} features")
    print(f"Class distribution: {df['target'].value_counts().to_dict()}")
    
    return df, feature_cols


def train_and_evaluate():
    """Main training pipeline."""
    print("=" * 60)
    print("LIVER DISEASE MODEL TRAINING (Real ILPD Data)")
    print("=" * 60)
    
    df, feature_cols = load_and_prepare_data()
    
    X = df[feature_cols]
    y = df['target']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )
    print(f"Training: {len(X_train)}, Test: {len(X_test)}")
    
    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=RANDOM_STATE, class_weight='balanced')
    
    cv = StratifiedKFold(n_splits=CV_FOLDS, shuffle=True, random_state=RANDOM_STATE)
    cv_scores = cross_val_score(model, X_train, y_train, cv=cv, scoring='roc_auc')
    print(f"CV AUC: {cv_scores.mean():.4f}")
    
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    
    metrics = {
        'accuracy': float(accuracy_score(y_test, y_pred)),
        'recall': float(recall_score(y_test, y_pred)),
        'roc_auc': float(roc_auc_score(y_test, y_proba)),
    }
    print(f"Test Accuracy: {metrics['accuracy']:.4f}")
    print(f"Test Recall: {metrics['recall']:.4f}")
    print(f"Test AUC: {metrics['roc_auc']:.4f}")
    
    explainer = shap.TreeExplainer(model)
    
    output_dir = OUTPUTS_DIR / "liver"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    joblib.dump(model, output_dir / "model.pkl")
    joblib.dump(explainer, output_dir / "shap_explainer.pkl")
    
    metadata = {
        "model_name": "RandomForest",
        "disease": "liver",
        "data_source": "Indian Liver Patient Dataset (UCI) - 583 patients",
        "features": feature_cols,
        "metrics": metrics,
        "trained_at": datetime.now().isoformat(),
    }
    with open(output_dir / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    
    print(f"✓ Saved to {output_dir}")


if __name__ == "__main__":
    train_and_evaluate()
