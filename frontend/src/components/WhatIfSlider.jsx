import { useState, useEffect } from 'react'
import { Sliders, RefreshCw } from 'lucide-react'
import './WhatIfSlider.css'

/**
 * What-If Analysis component with interactive sliders.
 * Allows users to adjust input values and see how predictions change.
 */
function WhatIfSlider({ fields, originalValues, onAnalyze, originalResult }) {
    const [modifiedValues, setModifiedValues] = useState({ ...originalValues })
    const [isAnalyzing, setIsAnalyzing] = useState(false)
    const [comparisonResult, setComparisonResult] = useState(null)

    const handleSliderChange = (name, value) => {
        setModifiedValues(prev => ({ ...prev, [name]: parseFloat(value) }))
    }

    const handleAnalyze = async () => {
        setIsAnalyzing(true)
        try {
            const result = await onAnalyze(originalValues, modifiedValues)
            setComparisonResult(result)
        } catch (err) {
            console.error('What-if analysis failed:', err)
        } finally {
            setIsAnalyzing(false)
        }
    }

    const handleReset = () => {
        setModifiedValues({ ...originalValues })
        setComparisonResult(null)
    }

    const hasChanges = Object.keys(originalValues).some(
        key => originalValues[key] !== modifiedValues[key]
    )

    return (
        <div className="what-if-container">
            <div className="what-if-header">
                <h3><Sliders size={20} /> What-If Analysis</h3>
                <p>Adjust values to see how they affect your risk assessment</p>
            </div>

            <div className="sliders-grid">
                {fields.filter(f => f.type === 'number').slice(0, 6).map(field => {
                    const originalVal = originalValues[field.name] || 0
                    const modifiedVal = modifiedValues[field.name] || 0
                    const isChanged = originalVal !== modifiedVal

                    return (
                        <div key={field.name} className={`slider-item ${isChanged ? 'changed' : ''}`}>
                            <div className="slider-header">
                                <label>{field.label}</label>
                                <div className="slider-values">
                                    <span className="original-value">{originalVal}</span>
                                    {isChanged && (
                                        <>
                                            <span className="arrow">→</span>
                                            <span className="modified-value">{modifiedVal}</span>
                                        </>
                                    )}
                                </div>
                            </div>
                            <input
                                type="range"
                                min={field.min}
                                max={field.max}
                                step={field.step || 1}
                                value={modifiedVal}
                                onChange={(e) => handleSliderChange(field.name, e.target.value)}
                                className="what-if-slider"
                            />
                        </div>
                    )
                })}
            </div>

            <div className="what-if-actions">
                <button
                    onClick={handleReset}
                    className="btn btn-secondary"
                    disabled={!hasChanges}
                >
                    <RefreshCw size={16} /> Reset
                </button>
                <button
                    onClick={handleAnalyze}
                    className="btn btn-primary"
                    disabled={!hasChanges || isAnalyzing}
                >
                    {isAnalyzing ? 'Analyzing...' : 'Compare Predictions'}
                </button>
            </div>

            {comparisonResult && (
                <div className="comparison-result">
                    <h4>Comparison Result</h4>
                    <div className="comparison-grid">
                        <div className="comparison-item original">
                            <span className="comparison-label">Original Risk</span>
                            <span className="comparison-value">
                                {Math.round(comparisonResult.original_prediction.probability * 100)}%
                            </span>
                        </div>
                        <div className="comparison-arrow">→</div>
                        <div className="comparison-item modified">
                            <span className="comparison-label">Modified Risk</span>
                            <span className="comparison-value">
                                {Math.round(comparisonResult.modified_prediction.probability * 100)}%
                            </span>
                        </div>
                    </div>
                    <div className={`probability-change ${comparisonResult.probability_change > 0 ? 'increased' : 'decreased'}`}>
                        Risk {comparisonResult.probability_change > 0 ? 'increased' : 'decreased'} by{' '}
                        {Math.abs(Math.round(comparisonResult.probability_change * 100))}%
                    </div>
                    {comparisonResult.key_changes.length > 0 && (
                        <div className="key-changes">
                            <strong>Changes made:</strong>
                            <ul>
                                {comparisonResult.key_changes.map((change, i) => (
                                    <li key={i}>{change}</li>
                                ))}
                            </ul>
                        </div>
                    )}
                </div>
            )}
        </div>
    )
}

export default WhatIfSlider
