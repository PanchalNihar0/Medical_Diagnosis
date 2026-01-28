"""
ML Pipeline Configuration.
"""
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

# Model settings
RANDOM_STATE = 42
TEST_SIZE = 0.2
CV_FOLDS = 5

# Feature names for each disease (human-readable mapping)
FEATURE_NAMES = {
    "diabetes": {
        "pregnancies": "Number of Pregnancies",
        "glucose": "Plasma Glucose (mg/dL)",
        "blood_pressure": "Blood Pressure (mm Hg)",
        "skin_thickness": "Skin Thickness (mm)",
        "insulin": "Insulin Level (mu U/ml)",
        "bmi": "BMI (kg/m²)",
        "diabetes_pedigree": "Diabetes Pedigree Function",
        "age": "Age (years)"
    },
    "heart": {
        "age": "Age (years)",
        "sex": "Sex",
        "chest_pain_type": "Chest Pain Type",
        "resting_bp": "Resting Blood Pressure",
        "cholesterol": "Cholesterol (mg/dL)",
        "fasting_blood_sugar": "Fasting Blood Sugar > 120",
        "resting_ecg": "Resting ECG Results",
        "max_heart_rate": "Maximum Heart Rate",
        "exercise_angina": "Exercise Induced Angina",
        "st_depression": "ST Depression",
        "st_slope": "ST Slope",
        "num_vessels": "Number of Major Vessels",
        "thalassemia": "Thalassemia Type"
    },
    "kidney": {
        "age": "Age (years)",
        "blood_pressure": "Blood Pressure (mm Hg)",
        "specific_gravity": "Specific Gravity",
        "albumin": "Albumin Level",
        "sugar": "Sugar Level",
        "red_blood_cells": "Red Blood Cells",
        "pus_cell": "Pus Cell",
        "pus_cell_clumps": "Pus Cell Clumps",
        "bacteria": "Bacteria",
        "blood_glucose": "Blood Glucose Random",
        "blood_urea": "Blood Urea",
        "serum_creatinine": "Serum Creatinine",
        "sodium": "Sodium (mEq/L)",
        "potassium": "Potassium (mEq/L)",
        "hemoglobin": "Hemoglobin (g/dL)",
        "packed_cell_volume": "Packed Cell Volume",
        "white_blood_cell_count": "WBC Count",
        "red_blood_cell_count": "RBC Count"
    },
    "liver": {
        "age": "Age (years)",
        "gender": "Gender",
        "total_bilirubin": "Total Bilirubin",
        "direct_bilirubin": "Direct Bilirubin",
        "alkaline_phosphatase": "Alkaline Phosphatase",
        "alamine_aminotransferase": "ALT (SGPT)",
        "aspartate_aminotransferase": "AST (SGOT)",
        "total_proteins": "Total Proteins",
        "albumin": "Albumin",
        "albumin_globulin_ratio": "A/G Ratio"
    }
}
