import { Heart, AlertCircle, ArrowRight, Info } from 'lucide-react'
import { useState } from 'react'
import { heartApi } from '../api/client'
import ResultsView from '../components/ResultsView'
import './Predictor.css'

const formFields = [
    { name: 'age', label: 'Age', type: 'number', min: 20, max: 100, placeholder: '55', unit: 'years' },
    { name: 'sex', label: 'Sex', type: 'select', options: [{ v: 0, l: 'Female' }, { v: 1, l: 'Male' }] },
    {
        name: 'chest_pain_type', label: 'Chest Pain Type', type: 'select',
        options: [{ v: 0, l: 'Typical Angina' }, { v: 1, l: 'Atypical Angina' }, { v: 2, l: 'Non-anginal' }, { v: 3, l: 'Asymptomatic' }]
    },
    { name: 'resting_bp', label: 'Resting Blood Pressure', type: 'number', min: 80, max: 200, placeholder: '130', unit: 'mm Hg' },
    { name: 'cholesterol', label: 'Cholesterol', type: 'number', min: 100, max: 600, placeholder: '250', unit: 'mg/dL' },
    { name: 'fasting_blood_sugar', label: 'Fasting Blood Sugar > 120 mg/dL', type: 'select', options: [{ v: 0, l: 'No' }, { v: 1, l: 'Yes' }] },
    {
        name: 'resting_ecg', label: 'Resting ECG', type: 'select',
        options: [{ v: 0, l: 'Normal' }, { v: 1, l: 'ST-T Abnormality' }, { v: 2, l: 'LV Hypertrophy' }]
    },
    { name: 'max_heart_rate', label: 'Max Heart Rate', type: 'number', min: 60, max: 220, placeholder: '150', unit: 'bpm' },
    { name: 'exercise_angina', label: 'Exercise Induced Angina', type: 'select', options: [{ v: 0, l: 'No' }, { v: 1, l: 'Yes' }] },
    { name: 'st_depression', label: 'ST Depression', type: 'number', min: 0, max: 10, step: 0.1, placeholder: '1.0' },
    {
        name: 'st_slope', label: 'ST Slope', type: 'select',
        options: [{ v: 0, l: 'Upsloping' }, { v: 1, l: 'Flat' }, { v: 2, l: 'Downsloping' }]
    },
    {
        name: 'num_vessels', label: 'Major Vessels Colored', type: 'select',
        options: [{ v: 0, l: '0' }, { v: 1, l: '1' }, { v: 2, l: '2' }, { v: 3, l: '3' }]
    },
    {
        name: 'thalassemia', label: 'Thalassemia', type: 'select',
        options: [{ v: 1, l: 'Normal' }, { v: 2, l: 'Fixed Defect' }, { v: 3, l: 'Reversible Defect' }]
    },
]

function HeartPredictor() {
    const [formData, setFormData] = useState({})
    const [errors, setErrors] = useState({})
    const [loading, setLoading] = useState(false)
    const [result, setResult] = useState(null)
    const [apiError, setApiError] = useState(null)

    const handleChange = (e) => {
        const { name, value } = e.target
        setFormData(prev => ({ ...prev, [name]: value }))
        if (errors[name]) setErrors(prev => ({ ...prev, [name]: null }))
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        const newErrors = {}
        formFields.forEach(f => {
            if (formData[f.name] === undefined || formData[f.name] === '') {
                newErrors[f.name] = 'Required'
            }
        })
        if (Object.keys(newErrors).length > 0) {
            setErrors(newErrors)
            return
        }

        setLoading(true)
        setApiError(null)
        try {
            const payload = {}
            formFields.forEach(f => { payload[f.name] = parseFloat(formData[f.name]) })
            const response = await heartApi.predict(payload)
            setResult(response)
        } catch (error) {
            setApiError(error.message || 'Prediction failed')
        } finally {
            setLoading(false)
        }
    }

    const handleReset = () => {
        setFormData({})
        setResult(null)
        setErrors({})
        setApiError(null)
    }

    return (
        <div className="predictor-page container fade-in">
            <div className="predictor-header">
                <div className="predictor-icon" style={{ background: 'linear-gradient(135deg, #ef4444 0%, #b91c1c 100%)' }}>
                    <Heart size={32} />
                </div>
                <div>
                    <h1>Heart Disease Risk Assessment</h1>
                    <p>Evaluate cardiovascular disease risk factors</p>
                </div>
            </div>

            {!result ? (
                <div className="predictor-content">
                    <form onSubmit={handleSubmit} className="predictor-form">
                        <div className="form-grid">
                            {formFields.map(field => (
                                <div key={field.name} className="form-group">
                                    <label className="form-label">{field.label}</label>
                                    {field.type === 'select' ? (
                                        <select
                                            name={field.name}
                                            value={formData[field.name] ?? ''}
                                            onChange={handleChange}
                                            className={`form-input ${errors[field.name] ? 'error' : ''}`}
                                        >
                                            <option value="">Select...</option>
                                            {field.options.map(o => <option key={o.v} value={o.v}>{o.l}</option>)}
                                        </select>
                                    ) : (
                                        <div className="input-with-unit">
                                            <input
                                                type="number"
                                                name={field.name}
                                                value={formData[field.name] || ''}
                                                onChange={handleChange}
                                                placeholder={field.placeholder}
                                                min={field.min}
                                                max={field.max}
                                                step={field.step || 1}
                                                className={`form-input ${errors[field.name] ? 'error' : ''}`}
                                            />
                                            {field.unit && <span className="input-unit">{field.unit}</span>}
                                        </div>
                                    )}
                                    {errors[field.name] && <span className="form-error">{errors[field.name]}</span>}
                                </div>
                            ))}
                        </div>
                        {apiError && <div className="alert alert-danger"><AlertCircle size={20} /><span>{apiError}</span></div>}
                        <div className="form-actions">
                            <button type="submit" className="btn btn-primary btn-lg" disabled={loading}>
                                {loading ? 'Analyzing...' : <><span>Analyze Risk</span><ArrowRight size={20} /></>}
                            </button>
                        </div>
                    </form>
                    <div className="predictor-info">
                        <h3><Info size={18} /> About This Assessment</h3>
                        <p>Evaluates heart disease risk based on clinical factors including ECG results, cholesterol, and exercise tests.</p>
                    </div>
                </div>
            ) : (
                <ResultsView result={result} onDownload={() => { }} onReset={handleReset} disease="Heart Disease" />
            )}
        </div>
    )
}

export default HeartPredictor
