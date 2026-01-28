import { Bug, Upload, Activity } from 'lucide-react'
import './Predictor.css'

function MalariaPredictor() {
    return (
        <div className="predictor-page container fade-in">
            <div className="predictor-header">
                <div className="predictor-icon" style={{ background: 'linear-gradient(135deg, #f59e0b 0%, #b45309 100%)' }}>
                    <Bug size={32} />
                </div>
                <div>
                    <h1>Malaria Detection</h1>
                    <p>Detect malaria parasites from blood smear images</p>
                </div>
            </div>

            <div className="card" style={{ textAlign: 'center', padding: '4rem' }}>
                <Upload size={48} style={{ color: 'var(--gray-300)', marginBottom: '1rem' }} />
                <h2>Image Upload Coming Soon</h2>
                <p>The malaria detection model (PyTorch CNN) is being trained. Check back soon!</p>
            </div>
        </div>
    )
}

export default MalariaPredictor
