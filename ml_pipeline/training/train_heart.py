"""
Heart Disease Model Training - Real UCI Cleveland Dataset.
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


def load_and_prepare_data():
    """Load UCI Heart Disease Cleveland dataset."""
    data_path = RAW_DATA_DIR / "heart.csv"
    
    if not data_path.exists():
        print("Downloading UCI Heart Disease (Cleveland) dataset...")
        # Direct UCI ML Repository URL - the processed Cleveland data
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"
        
        columns = ['age', 'sex', 'chest_pain_type', 'resting_bp', 'cholesterol',
                   'fasting_blood_sugar', 'resting_ecg', 'max_heart_rate',
                   'exercise_angina', 'st_depression', 'st_slope', 'num_vessels',
                   'thalassemia', 'target']
        
        df = pd.read_csv(url, names=columns, na_values='?')
        
        # Handle missing values
        df = df.dropna()
        
        # Convert target: 0 = no disease, 1-4 = disease -> binary
        df['target'] = (df['target'] > 0).astype(int)
        
        RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
        df.to_csv(data_path, index=False)
        print(f"Saved {len(df)} samples to {data_path}")
    else:
        df = pd.read_csv(data_path)
    
    print(f"Loaded {len(df)} real samples from UCI Cleveland dataset")
    print(f"Class distribution: {df['target'].value_counts().to_dict()}")
    return df


def train_and_evaluate():
    """Main training pipeline with real data."""
    print("=" * 60)
    print("HEART DISEASE MODEL TRAINING (UCI Cleveland Data)")
    print("=" * 60)
    
    df = load_and_prepare_data()
    
    feature_cols = ['age', 'sex', 'chest_pain_type', 'resting_bp', 'cholesterol',
                    'fasting_blood_sugar', 'resting_ecg', 'max_heart_rate',
                    'exercise_angina', 'st_depression', 'st_slope', 'num_vessels', 'thalassemia']
    
    X = df[feature_cols]
    y = df['target']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )
    print(f"Training: {len(X_train)}, Test: {len(X_test)}")
    
    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=RANDOM_STATE, class_weight='balanced')
    
    cv = StratifiedKFold(n_splits=CV_FOLDS, shuffle=True, random_state=RANDOM_STATE)
    cv_scores = cross_val_score(model, X_train, y_train, cv=cv, scoring='roc_auc')
    print(f"CV AUC: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
    
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
    
    output_dir = OUTPUTS_DIR / "heart"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    joblib.dump(model, output_dir / "model.pkl")
    joblib.dump(explainer, output_dir / "shap_explainer.pkl")
    
    metadata = {
        "model_name": "RandomForest",
        "disease": "heart",
        "version": "2.0.0",
        "data_source": "UCI Heart Disease Cleveland",
        "trained_at": datetime.now().isoformat(),
        "features": feature_cols,
        "metrics": metrics,
        "training_samples": len(X_train),
        "test_samples": len(X_test),
        "model_type": "sklearn",
    }
    with open(output_dir / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    
    print(f"✓ Saved to {output_dir}")


if __name__ == "__main__":
    train_and_evaluate()
