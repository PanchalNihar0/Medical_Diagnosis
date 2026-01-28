# Architecture Documentation

## System Overview

MediScreen is a three-tier medical risk assessment application:

```
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND                                │
│                    React + Vite                              │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────────────┐   │
│  │  Pages  │ │Components│ │  Hooks  │ │   API Client    │   │
│  └─────────┘ └─────────┘ └─────────┘ └─────────────────┘   │
└───────────────────────────┬─────────────────────────────────┘
                            │ REST API
┌───────────────────────────▼─────────────────────────────────┐
│                       BACKEND                                │
│                      FastAPI                                 │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────────┐  │
│  │  Routes  │ │  Schemas │ │ Services │ │  ML Inference │  │
│  └──────────┘ └──────────┘ └──────────┘ └───────────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                    ML PIPELINE                               │
│               Training + Model Storage                       │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────────┐  │
│  │ Training │ │  Models  │ │   SHAP   │ │   Metadata    │  │
│  │ Scripts  │ │ (.pkl)   │ │Explainers│ │   (.json)     │  │
│  └──────────┘ └──────────┘ └──────────┘ └───────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Backend Architecture

### FastAPI Application (`backend/app/`)

```
app/
├── main.py              # FastAPI app factory, route registration
├── config.py            # Settings, logging configuration
├── api/
│   ├── routes/          # One file per disease + health + report
│   │   ├── diabetes.py  # /api/v1/diabetes/* endpoints
│   │   ├── heart.py     # /api/v1/heart/* endpoints
│   │   └── ...
│   └── schemas/         # Pydantic input/output models
│       ├── common.py    # Shared schemas (PredictionResult)
│       ├── diabetes.py  # DiabetesInput validation
│       └── ...
├── ml/
│   ├── registry.py      # Model loading with caching
│   └── inference.py     # TabularInference with SHAP
└── services/
    └── report.py        # PDF generation with ReportLab
```

### Request Flow

1. **Validation**: Pydantic schema validates and coerces input types
2. **Inference**: TabularInference loads model, runs prediction
3. **Explanation**: SHAP values computed for feature importance
4. **Response**: Structured response with probability, confidence, factors

### Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| FastAPI over Flask | Async support, automatic OpenAPI, Pydantic integration |
| Calibrated models | Honest probability estimates, not overconfident |
| SHAP (not LIME) | Theoretically grounded, consistent for tree models |
| Singleton model loading | Avoid re-loading models per request |

## Frontend Architecture

### React Application (`frontend/src/`)

```
src/
├── main.jsx             # App entry, BrowserRouter setup
├── App.jsx              # Route definitions
├── index.css            # Design system (CSS variables)
├── api/
│   └── client.js        # Fetch wrapper for all API calls
├── components/
│   ├── Layout.jsx       # Header, footer, navigation
│   ├── ConfidenceMeter  # Visual probability display
│   ├── ResultsView      # Full results with factors
│   ├── WhatIfSlider     # Interactive analysis
│   ├── HistoryPanel     # Past predictions
│   └── RiskChart        # Population comparison
├── hooks/
│   └── useLocalHistory  # localStorage persistence
└── pages/
    ├── Home.jsx         # Landing page
    ├── DiabetesPredictor # Full-featured predictor
    ├── HeartPredictor   # Heart disease form
    └── About.jsx        # Project information
```

### State Management

- **Local state**: React useState for form data, results
- **Persistence**: localStorage via useLocalHistory hook
- **No global state**: Each predictor is self-contained

## ML Pipeline Architecture

### Training Scripts (`ml_pipeline/training/`)

Each disease has a dedicated training script:

```python
def train_and_evaluate():
    # 1. Load data
    # 2. Preprocess (imputation, encoding)
    # 3. Train/test split (stratified)
    # 4. Cross-validation
    # 5. Model selection
    # 6. Calibration
    # 7. SHAP explainer
    # 8. Save artifacts
```

### Model Artifacts (`ml_pipeline/outputs/{disease}/`)

```
diabetes/
├── model.pkl           # Trained, calibrated model
├── shap_explainer.pkl  # TreeExplainer or KernelExplainer
└── metadata.json       # Features, metrics, version
```

### Metadata Schema

```json
{
  "model_name": "RandomForest",
  "disease": "diabetes",
  "version": "2.0.0",
  "trained_at": "2024-01-28T10:00:00",
  "features": ["glucose", "bmi", ...],
  "feature_names": {"glucose": "Plasma Glucose (mg/dL)"},
  "metrics": {"accuracy": 0.78, "recall": 0.82, "roc_auc": 0.85},
  "model_type": "sklearn"
}
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/health | Health check |
| POST | /api/v1/{disease}/predict | Get prediction |
| POST | /api/v1/{disease}/what-if | Compare scenarios |
| GET | /api/v1/{disease}/info | Model metadata |
| POST | /api/v1/report/generate | Generate PDF |

## Security Considerations

1. **No PII storage**: Predictions not persisted server-side
2. **Input validation**: Strict Pydantic schemas with ranges
3. **CORS configured**: Allow frontend origin only
4. **Disclaimers**: Medical disclaimers on every result

## Performance

- **Model caching**: LRU cache for loaded models
- **Lazy loading**: Models loaded on first request
- **Frontend optimization**: Vite code splitting, tree shaking
