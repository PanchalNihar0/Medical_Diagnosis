import { Ribbon, Activity } from 'lucide-react'
import './Predictor.css'

function BreastCancerPredictor() {
    return (
        <div className="predictor-page container fade-in">
            <div className="predictor-header">
                <div className="predictor-icon" style={{ background: 'linear-gradient(135deg, #ec4899 0%, #be185d 100%)' }}>
                    <Ribbon size={32} />
                </div>
                <div>
                    <h1>Breast Cancer Risk Assessment</h1>
                    <p>Analyze tumor characteristics for malignancy assessment</p>
                </div>
            </div>

            <div className="card" style={{ textAlign: 'center', padding: '4rem' }}>
                <Activity size={48} style={{ color: 'var(--gray-300)', marginBottom: '1rem' }} />
                <h2>Coming Soon</h2>
                <p>The breast cancer prediction model is being trained. Check back soon!</p>
            </div>
        </div>
    )
}

export default BreastCancerPredictor
