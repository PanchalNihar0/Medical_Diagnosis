import { FlaskConical, Info, Activity } from 'lucide-react'
import './Predictor.css'

function LiverPredictor() {
    return (
        <div className="predictor-page container fade-in">
            <div className="predictor-header">
                <div className="predictor-icon" style={{ background: 'linear-gradient(135deg, #10b981 0%, #047857 100%)' }}>
                    <FlaskConical size={32} />
                </div>
                <div>
                    <h1>Liver Disease Risk Assessment</h1>
                    <p>Assess liver function and disease risk</p>
                </div>
            </div>

            <div className="card" style={{ textAlign: 'center', padding: '4rem' }}>
                <Activity size={48} style={{ color: 'var(--gray-300)', marginBottom: '1rem' }} />
                <h2>Coming Soon</h2>
                <p>The liver disease prediction model is being trained. Check back soon!</p>
            </div>
        </div>
    )
}

export default LiverPredictor
