import { Clock, Trash2, X, ChevronDown, ChevronUp } from 'lucide-react'
import { useState } from 'react'
import './HistoryPanel.css'

/**
 * History Panel showing past predictions.
 */
function HistoryPanel({ history, onDeleteEntry, onClearAll, onClose }) {
    const [isExpanded, setIsExpanded] = useState(true)

    if (!history || history.length === 0) {
        return null
    }

    const formatDate = (isoString) => {
        const date = new Date(isoString)
        return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }

    const getRiskColor = (prediction, probability) => {
        if (prediction === 0) return 'low-risk'
        if (probability >= 0.7) return 'high-risk'
        return 'medium-risk'
    }

    return (
        <div className="history-panel">
            <div className="history-header" onClick={() => setIsExpanded(!isExpanded)}>
                <div className="history-title">
                    <Clock size={18} />
                    <span>Recent Assessments ({history.length})</span>
                </div>
                <div className="history-actions">
                    {isExpanded && history.length > 0 && (
                        <button
                            onClick={(e) => { e.stopPropagation(); onClearAll(); }}
                            className="clear-all-btn"
                            title="Clear all history"
                        >
                            Clear All
                        </button>
                    )}
                    {isExpanded ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
                </div>
            </div>

            {isExpanded && (
                <div className="history-list">
                    {history.slice(0, 10).map(entry => (
                        <div key={entry.id} className="history-item">
                            <div className="history-item-content">
                                <div className="history-item-header">
                                    <span className="history-disease">{entry.disease}</span>
                                    <span className="history-date">{formatDate(entry.timestamp)}</span>
                                </div>
                                <div className="history-item-result">
                                    <span className={`history-risk ${getRiskColor(entry.prediction, entry.probability)}`}>
                                        {entry.prediction === 0 ? 'Low Risk' : 'Elevated Risk'}
                                    </span>
                                    <span className="history-probability">
                                        {Math.round(entry.probability * 100)}%
                                    </span>
                                </div>
                            </div>
                            <button
                                onClick={() => onDeleteEntry(entry.id)}
                                className="history-delete-btn"
                                title="Delete entry"
                            >
                                <X size={14} />
                            </button>
                        </div>
                    ))}
                </div>
            )}
        </div>
    )
}

export default HistoryPanel
