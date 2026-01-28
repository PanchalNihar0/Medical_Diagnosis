import { Droplets, Info, Activity } from 'lucide-react'
import './Predictor.css'

function KidneyPredictor() {
    return (
        <div className="predictor-page container fade-in">
            <div className="predictor-header">
                <div className="predictor-icon" style={{ background: 'linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%)' }}>
                    <Droplets size={32} />
                </div>
                <div>
                    <h1>Kidney Disease Risk Assessment</h1>
                    <p>Screen for chronic kidney disease indicators</p>
                </div>
            </div>

            <div className="card" style={{ textAlign: 'center', padding: '4rem' }}>
                <Activity size={48} style={{ color: 'var(--gray-300)', marginBottom: '1rem' }} />
                <h2>Coming Soon</h2>
                <p>The kidney disease prediction model is being trained. Check back soon!</p>
            </div>
        </div>
    )
}

export default KidneyPredictor
