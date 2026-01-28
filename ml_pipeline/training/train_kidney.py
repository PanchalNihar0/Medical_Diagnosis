"""
Kidney Disease Model Training - Real UCI CKD Dataset.
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
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, recall_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import OUTPUTS_DIR, RAW_DATA_DIR, RANDOM_STATE, TEST_SIZE, CV_FOLDS

warnings.filterwarnings('ignore')


def load_and_prepare_data():
    """Load UCI Chronic Kidney Disease dataset."""
    data_path = RAW_DATA_DIR / "kidney.csv"
    
    if not data_path.exists():
        print("Downloading Chronic Kidney Disease dataset...")
        
        # Verified working URLs
        urls = [
            "https://raw.githubusercontent.com/aiplanethub/Datasets/master/ChronicKidneyDisease.csv",
            "https://raw.githubusercontent.com/ArjunAnilPillai/Chronic-Kidney-Disease-dataset/master/kidney_disease.csv",
        ]
        
        df = None
        for url in urls:
            try:
                print(f"Trying: {url}")
                df = pd.read_csv(url)
                print(f"✓ Downloaded from: {url}")
                break
            except Exception as e:
                print(f"✗ Failed: {e}")
                continue
        
        if df is None:
            raise RuntimeError("Could not download kidney disease dataset")
        
        RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
        df.to_csv(data_path, index=False)
        print(f"Saved to {data_path}")
    else:
        df = pd.read_csv(data_path)
    
    return prepare_ckd_data(df)


def prepare_ckd_data(df):
    """Clean and prepare the CKD dataset."""
    df.columns = df.columns.str.strip().str.lower()
    
    # Replace ? with NaN
    df = df.replace(['?', '\t?', '', ' '], np.nan)
    
    # Find target column
    target_col = None
    for col in ['classification', 'class', 'ckd']:
        if col in df.columns:
            target_col = col
            break
    
    if target_col is None:
        target_col = df.columns[-1]
    
    # Convert target to binary (ckd = 1, notckd = 0)
    df['target'] = df[target_col].apply(
        lambda x: 1 if str(x).strip().lower() in ['ckd', 'ckd\t', '1', '1.0', 'yes'] else 0
    )
    
    # Select numeric columns
    numeric_cols = []
    for col in df.columns:
        if col in ['target', target_col, 'id']:
            continue
        try:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            if df[col].notna().sum() > len(df) * 0.3:  # At least 30% non-null
                numeric_cols.append(col)
        except:
            continue
    
    # Keep only numeric + target
    df = df[numeric_cols + ['target']]
    
    print(f"Loaded {len(df)} samples with {len(numeric_cols)} features")
    print(f"Class distribution: {df['target'].value_counts().to_dict()}")
    return df, numeric_cols


def train_and_evaluate():
    """Main training pipeline."""
    print("=" * 60)
    print("KIDNEY DISEASE MODEL TRAINING (Real CKD Data)")
    print("=" * 60)
    
    df, feature_cols = load_and_prepare_data()
    
    X = df[feature_cols].copy()
    y = df['target']
    
    # Impute missing values
    imputer = SimpleImputer(strategy='median')
    X = pd.DataFrame(imputer.fit_transform(X), columns=feature_cols)
    
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
    
    output_dir = OUTPUTS_DIR / "kidney"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    joblib.dump(model, output_dir / "model.pkl")
    joblib.dump(explainer, output_dir / "shap_explainer.pkl")
    joblib.dump(imputer, output_dir / "imputer.pkl")
    
    metadata = {
        "model_name": "RandomForest",
        "disease": "kidney",
        "data_source": "UCI Chronic Kidney Disease Dataset",
        "features": feature_cols,
        "metrics": metrics,
        "trained_at": datetime.now().isoformat(),
    }
    with open(output_dir / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    
    print(f"✓ Saved to {output_dir}")


if __name__ == "__main__":
    train_and_evaluate()
