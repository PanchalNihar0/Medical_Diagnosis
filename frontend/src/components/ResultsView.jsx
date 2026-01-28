import { AlertTriangle, Download, RefreshCw, Check, TrendingUp, TrendingDown, ArrowRight } from 'lucide-react'
import ConfidenceMeter from './ConfidenceMeter'

function ResultsView({ result, onDownload, onReset, disease }) {
    const { result: prediction, warnings, input_summary } = result

    const isHighRisk = prediction.prediction === 1

    return (
        <div className="results-container">
            {/* Disclaimer */}
            <div className="result-disclaimer">
                <AlertTriangle size={20} />
                <p>{prediction.disclaimer}</p>
            </div>

            <div className="results-grid">
                {/* Main Result Card */}
                <div className="result-card">
                    <h3>Risk Assessment</h3>
                    <div className="risk-assessment">
                        <div className={`risk-icon ${isHighRisk ? 'high-risk' : 'low-risk'}`}>
                            {isHighRisk ? <TrendingUp size={40} /> : <Check size={40} />}
                        </div>
                        <h2 className={`risk-title ${isHighRisk ? 'high-risk' : 'low-risk'}`}>
                            {isHighRisk ? 'Elevated Risk Detected' : 'Low Risk Indicated'}
                        </h2>
                        <p className="risk-description">
                            {prediction.recommendation}
                        </p>
                    </div>
                </div>

                {/* Confidence Card */}
                <div className="result-card">
                    <h3>Confidence Level</h3>
                    <ConfidenceMeter
                        probability={prediction.probability}
                        confidenceLevel={prediction.confidence_level}
                        prediction={prediction.prediction}
                    />
                    <p style={{ fontSize: '0.875rem', color: 'var(--gray-500)', marginTop: 'var(--space-4)' }}>
                        {prediction.confidence_level === 'HIGH'
                            ? 'The model is highly confident in this assessment.'
                            : prediction.confidence_level === 'MEDIUM'
                                ? 'The model has moderate confidence. Consider consulting a healthcare provider.'
                                : 'The model confidence is low. Results are inconclusive.'}
                    </p>
                </div>

                {/* Contributing Factors */}
                {prediction.top_factors && prediction.top_factors.length > 0 && (
                    <div className="result-card">
                        <h3>Key Contributing Factors</h3>
                        <div className="factors-list">
                            {prediction.top_factors.map((factor, index) => (
                                <div key={index} className="factor-item">
                                    <div className={`factor-impact ${factor.contribution > 0 ? 'positive' : 'negative'}`}>
                                        {factor.contribution > 0 ? <TrendingUp size={18} /> : <TrendingDown size={18} />}
                                    </div>
                                    <div className="factor-content">
                                        <div className="factor-name">{factor.display_name}</div>
                                        <div className="factor-interpretation">{factor.interpretation}</div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {/* Recommendations */}
                {prediction.lifestyle_tips && prediction.lifestyle_tips.length > 0 && (
                    <div className="result-card">
                        <h3>Recommendations</h3>
                        <div className="recommendations-list">
                            {prediction.lifestyle_tips.map((tip, index) => (
                                <div key={index} className="recommendation-item">
                                    <Check size={18} />
                                    <span>{tip}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {/* Warnings */}
                {warnings && warnings.length > 0 && (
                    <div className="result-card full-width">
                        <h3>Clinical Warnings</h3>
                        {warnings.map((warning, index) => (
                            <div key={index} className="alert alert-warning" style={{ marginBottom: 'var(--space-2)' }}>
                                <AlertTriangle size={18} />
                                <span>{warning}</span>
                            </div>
                        ))}
                    </div>
                )}
            </div>

            {/* Actions */}
            <div className="results-actions">
                <button onClick={onReset} className="btn btn-secondary btn-lg">
                    <RefreshCw size={18} />
                    New Assessment
                </button>
                <button onClick={onDownload} className="btn btn-primary btn-lg">
                    <Download size={18} />
                    Download PDF Report
                </button>
            </div>
        </div>
    )
}

export default ResultsView
