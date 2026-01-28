import { Wind, Upload } from 'lucide-react'
import './Predictor.css'

function PneumoniaPredictor() {
    return (
        <div className="predictor-page container fade-in">
            <div className="predictor-header">
                <div className="predictor-icon" style={{ background: 'linear-gradient(135deg, #06b6d4 0%, #0e7490 100%)' }}>
                    <Wind size={32} />
                </div>
                <div>
                    <h1>Pneumonia Detection</h1>
                    <p>Analyze chest X-rays for pneumonia indicators</p>
                </div>
            </div>

            <div className="card" style={{ textAlign: 'center', padding: '4rem' }}>
                <Upload size={48} style={{ color: 'var(--gray-300)', marginBottom: '1rem' }} />
                <h2>Image Upload Coming Soon</h2>
                <p>The pneumonia detection model (PyTorch CNN) is being trained. Check back soon!</p>
            </div>
        </div>
    )
}

export default PneumoniaPredictor
