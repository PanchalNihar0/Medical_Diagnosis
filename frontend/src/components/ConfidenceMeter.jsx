import './ConfidenceMeter.css'

function ConfidenceMeter({ probability, confidenceLevel, prediction }) {
    const percentage = Math.round(probability * 100)

    // Determine visual class
    let barClass = 'low'
    if (confidenceLevel === 'HIGH') {
        barClass = prediction === 1 ? 'high-risk' : 'high-safe'
    } else if (confidenceLevel === 'MEDIUM') {
        barClass = 'medium'
    }

    const levelText = {
        LOW: 'Low Confidence',
        MEDIUM: 'Moderate Confidence',
        HIGH: 'High Confidence'
    }

    return (
        <div className="confidence-meter">
            <div className="confidence-bar-container">
                <div
                    className={`confidence-bar-fill ${barClass}`}
                    style={{ width: `${percentage}%` }}
                />
            </div>
            <div className="confidence-info">
                <span className={`confidence-level badge badge-${confidenceLevel.toLowerCase()}`}>
                    {levelText[confidenceLevel]}
                </span>
                <span className="confidence-probability">
                    {percentage}%
                </span>
            </div>
        </div>
    )
}

export default ConfidenceMeter
