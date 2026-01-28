# MediScreen - AI Health Risk Assessment

<div align="center">
  <img src="docs/logo.png" alt="MediScreen Logo" width="120" />
  <h3>AI-Powered Medical Risk Screening System</h3>
  <p>Transparent, explainable health risk assessments for educational and screening purposes</p>
</div>

---

## 🎯 Overview

MediScreen is a modern web application that uses machine learning to provide health risk assessments for 7 common conditions:

| Condition | Input Type | Model |
|-----------|------------|-------|
| Diabetes | Clinical values | RandomForest/GradientBoosting |
| Heart Disease | Clinical values | RandomForest |
| Kidney Disease | Lab values | RandomForest |
| Liver Disease | Lab values | RandomForest |
| Breast Cancer | Biopsy data | RandomForest |
| Malaria | Cell images | PyTorch CNN |
| Pneumonia | X-ray images | PyTorch CNN |

### Key Features

- **Explainable AI**: SHAP-based explanations show which factors influenced the prediction
- **Confidence Scoring**: Honest probability estimates with calibrated models
- **What-If Analysis**: See how changing factors affects your risk
- **PDF Reports**: Download formatted summaries to share with healthcare providers
- **Responsible Messaging**: Clear disclaimers and appropriate recommendations

---

## ⚠️ Important Disclaimer

> **This is a screening tool, NOT a diagnostic system.**
> 
> Results are educational and should not replace professional medical evaluation. 
> A "low risk" result does NOT mean you are healthy. A "high risk" result does NOT 
> mean you have a disease. Always consult qualified healthcare professionals.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm 9+

### 1. Clone and Setup

```bash
git clone <repository-url>
cd Medical_Diagnosis
```

### 2. Backend Setup

```bash
# Create virtual environment
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the API server
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`  
API docs at `http://localhost:8000/docs`

### 3. Train Models (First Time)

```bash
cd ml_pipeline/training
python train_all.py
```

This will train models and save them to `ml_pipeline/outputs/`.

### 4. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173`

---

## 📁 Project Structure

```
Medical_Diagnosis/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/routes/      # API endpoints
│   │   ├── api/schemas/     # Pydantic models
│   │   ├── ml/              # Model loading & inference
│   │   └── services/        # PDF reports, etc.
│   └── tests/
├── ml_pipeline/             # ML training pipeline
│   ├── training/            # Training scripts
│   ├── data/raw/            # Datasets
│   └── outputs/             # Trained models
├── frontend/                # React + Vite frontend
│   └── src/
│       ├── components/      # UI components
│       ├── pages/           # Page components
│       └── api/             # API client
└── docs/                    # Documentation
```

---

## 🔧 Technology Stack

### Backend
- **FastAPI** - Modern async Python web framework
- **Pydantic** - Data validation and serialization
- **scikit-learn** - Tabular ML models
- **PyTorch** - Image classification models
- **SHAP** - Model explainability
- **ReportLab** - PDF generation

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool
- **React Router** - Client-side routing
- **Lucide React** - Icons
- **Recharts** - Charts

---

## 📊 Model Methodology

Our training pipeline ensures responsible ML:

1. **Proper Evaluation**: Stratified train/test splits, cross-validation
2. **Honest Metrics**: We report realistic accuracy, not inflated claims
3. **Calibration**: Probability calibration for reliable confidence estimates
4. **Recall Priority**: Medical screening prioritizes minimizing false negatives
5. **Explainability**: SHAP values for every prediction

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- Datasets from [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/index.php)
- SHAP library by [Scott Lundberg](https://github.com/slundberg/shap)
