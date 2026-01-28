import { useState } from 'react'
import { Activity, AlertCircle, ArrowRight, Info } from 'lucide-react'
import { diabetesApi, reportApi } from '../api/client'
import ResultsView from '../components/ResultsView'
import WhatIfSlider from '../components/WhatIfSlider'
import RiskChart from '../components/RiskChart'
import HistoryPanel from '../components/HistoryPanel'
import useLocalHistory from '../hooks/useLocalHistory'
import './Predictor.css'

const formFields = [
    { name: 'pregnancies', label: 'Number of Pregnancies', type: 'number', min: 0, max: 20, step: 1, placeholder: '0', hint: 'Total number of pregnancies', unit: '' },
    { name: 'glucose', label: 'Plasma Glucose', type: 'number', min: 40, max: 300, step: 1, placeholder: '120', hint: '2-hour oral glucose tolerance test result', unit: 'mg/dL' },
    { name: 'blood_pressure', label: 'Blood Pressure', type: 'number', min: 40, max: 150, step: 1, placeholder: '72', hint: 'Diastolic blood pressure', unit: 'mm Hg' },
    { name: 'skin_thickness', label: 'Skin Thickness', type: 'number', min: 0, max: 100, step: 1, placeholder: '23', hint: 'Triceps skin fold thickness', unit: 'mm' },
    { name: 'insulin', label: 'Insulin Level', type: 'number', min: 0, max: 1000, step: 1, placeholder: '85', hint: '2-hour serum insulin', unit: 'mu U/ml' },
    { name: 'bmi', label: 'Body Mass Index (BMI)', type: 'number', min: 10, max: 70, step: 0.1, placeholder: '28.5', hint: 'Weight in kg / (height in m)²', unit: 'kg/m²' },
    { name: 'diabetes_pedigree', label: 'Diabetes Pedigree Function', type: 'number', min: 0, max: 3, step: 0.01, placeholder: '0.52', hint: 'Genetic risk score based on family history', unit: '' },
    { name: 'age', label: 'Age', type: 'number', min: 1, max: 120, step: 1, placeholder: '45', hint: 'Age in years', unit: 'years' },
]

function DiabetesPredictor() {
    const [formData, setFormData] = useState({})
    const [errors, setErrors] = useState({})
    const [loading, setLoading] = useState(false)
    const [result, setResult] = useState(null)
    const [apiError, setApiError] = useState(null)
    const [showWhatIf, setShowWhatIf] = useState(false)

    const { history, addToHistory, getHistoryByDisease, clearDiseaseHistory, deleteEntry } = useLocalHistory()
    const diabetesHistory = getHistoryByDisease('diabetes')

    const handleChange = (e) => {
        const { name, value } = e.target
        setFormData(prev => ({ ...prev, [name]: value }))
        if (errors[name]) setErrors(prev => ({ ...prev, [name]: null }))
    }

    const validateForm = () => {
        const newErrors = {}
        formFields.forEach(field => {
            const value = formData[field.name]
            if (value === undefined || value === '') {
                newErrors[field.name] = 'This field is required'
            } else {
                const numValue = parseFloat(value)
                if (isNaN(numValue)) newErrors[field.name] = 'Must be a number'
                else if (numValue < field.min || numValue > field.max) newErrors[field.name] = `Must be between ${field.min} and ${field.max}`
            }
        })
        setErrors(newErrors)
        return Object.keys(newErrors).length === 0
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        if (!validateForm()) return

        setLoading(true)
        setApiError(null)
        try {
            const payload = {}
            formFields.forEach(field => { payload[field.name] = parseFloat(formData[field.name]) })
            const response = await diabetesApi.predict(payload)
            setResult(response)
            addToHistory('diabetes', payload, response)
        } catch (error) {
            setApiError(error.message || 'Failed to get prediction. Please try again.')
        } finally {
            setLoading(false)
        }
    }

    const handleWhatIfAnalyze = async (original, modified) => {
        return await diabetesApi.whatIf({ original_inputs: original, modified_inputs: modified })
    }

    const handleDownloadReport = async () => {
        if (!result) return
        try {
            const blob = await reportApi.generate({
                prediction_result: result.result,
                patient_inputs: formData,
                include_recommendations: true,
                include_explanations: true,
            })
            const url = window.URL.createObjectURL(blob)
            const a = document.createElement('a')
            a.href = url
            a.download = 'diabetes-risk-assessment.pdf'
            document.body.appendChild(a)
            a.click()
            document.body.removeChild(a)
            window.URL.revokeObjectURL(url)
        } catch (error) {
            setApiError('Failed to generate PDF report')
        }
    }

    const handleReset = () => {
        setFormData({})
        setResult(null)
        setErrors({})
        setApiError(null)
        setShowWhatIf(false)
    }

    return (
        <div className="predictor-page container fade-in">
            <div className="predictor-header">
                <div className="predictor-icon" style={{ background: 'linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)' }}>
                    <Activity size={32} />
                </div>
                <div>
                    <h1>Diabetes Risk Assessment</h1>
                    <p>Enter your clinical values to assess Type 2 diabetes risk</p>
                </div>
            </div>

            {diabetesHistory.length > 0 && !result && (
                <HistoryPanel
                    history={diabetesHistory}
                    onDeleteEntry={deleteEntry}
                    onClearAll={() => clearDiseaseHistory('diabetes')}
                />
            )}

            {!result ? (
                <div className="predictor-content">
                    <form onSubmit={handleSubmit} className="predictor-form">
                        <div className="form-grid">
                            {formFields.map(field => (
                                <div key={field.name} className="form-group">
                                    <label className="form-label">
                                        {field.label}
                                        {field.unit && <span className="label-unit">({field.unit})</span>}
                                    </label>
                                    <div className="input-with-unit">
                                        <input
                                            type={field.type}
                                            name={field.name}
                                            value={formData[field.name] || ''}
                                            onChange={handleChange}
                                            placeholder={field.placeholder}
                                            min={field.min}
                                            max={field.max}
                                            step={field.step}
                                            className={`form-input ${errors[field.name] ? 'error' : ''}`}
                                        />
                                        {field.unit && <span className="input-unit">{field.unit}</span>}
                                    </div>
                                    {field.hint && !errors[field.name] && <span className="form-hint">{field.hint}</span>}
                                    {errors[field.name] && <span className="form-error">{errors[field.name]}</span>}
                                </div>
                            ))}
                        </div>

                        {apiError && <div className="alert alert-danger"><AlertCircle size={20} /><span>{apiError}</span></div>}

                        <div className="form-actions">
                            <button type="submit" className="btn btn-primary btn-lg" disabled={loading}>
                                {loading ? <><span className="spinner" style={{ width: '1.25rem', height: '1.25rem' }}></span>Analyzing...</> : <>Analyze Risk<ArrowRight size={20} /></>}
                            </button>
                        </div>
                    </form>

                    <div className="predictor-info">
                        <h3><Info size={18} /> About This Assessment</h3>
                        <p>This tool uses machine learning to assess Type 2 diabetes risk based on clinical measurements.</p>
                        <h4>Required Information</h4>
                        <ul>
                            <li>Results from an oral glucose tolerance test</li>
                            <li>Blood pressure measurements</li>
                            <li>Body measurements (BMI, skin thickness)</li>
                            <li>Insulin levels</li>
                            <li>Family history (diabetes pedigree function)</li>
                        </ul>
                    </div>
                </div>
            ) : (
                <>
                    <ResultsView result={result} onDownload={handleDownloadReport} onReset={handleReset} disease="Diabetes" />

                    <RiskChart probability={result.result.probability} disease="diabetes" populationAverage={0.13} />

                    <div style={{ marginTop: 'var(--space-4)' }}>
                        <button onClick={() => setShowWhatIf(!showWhatIf)} className="btn btn-outline">
                            {showWhatIf ? 'Hide What-If Analysis' : 'Try What-If Analysis'}
                        </button>
                    </div>

                    {showWhatIf && (
                        <WhatIfSlider
                            fields={formFields}
                            originalValues={Object.fromEntries(formFields.map(f => [f.name, parseFloat(formData[f.name])]))}
                            onAnalyze={handleWhatIfAnalyze}
                            originalResult={result}
                        />
                    )}
                </>
            )}
        </div>
    )
}

export default DiabetesPredictor
