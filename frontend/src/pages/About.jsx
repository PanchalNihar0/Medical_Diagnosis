import { Shield, Brain, Code, AlertTriangle, CheckCircle } from 'lucide-react'
import './About.css'

function About() {
    return (
        <div className="about-page container fade-in">
            <div className="about-header">
                <h1>About MediScreen</h1>
                <p>AI-powered health risk assessment for educational and screening purposes</p>
            </div>

            <div className="about-grid">
                <section className="about-section">
                    <h2><Brain size={24} /> What It Does</h2>
                    <p>
                        MediScreen uses machine learning models trained on validated medical datasets
                        to provide risk assessments for various health conditions. The system analyzes
                        clinical inputs and provides:
                    </p>
                    <ul>
                        <li>Risk probability with confidence levels</li>
                        <li>Explainable AI - see which factors contributed to the assessment</li>
                        <li>Lifestyle recommendations based on risk factors</li>
                        <li>Downloadable PDF reports for healthcare consultations</li>
                    </ul>
                </section>

                <section className="about-section">
                    <h2><Shield size={24} /> What It Does NOT Do</h2>
                    <div className="warning-box">
                        <AlertTriangle size={20} />
                        <div>
                            <strong>This is NOT a diagnostic tool</strong>
                            <p>
                                MediScreen provides risk assessments, not medical diagnoses.
                                It should never be used as a substitute for professional medical
                                evaluation, testing, or treatment.
                            </p>
                        </div>
                    </div>
                    <ul>
                        <li>Does not diagnose diseases</li>
                        <li>Does not recommend treatments or medications</li>
                        <li>Does not replace laboratory tests</li>
                        <li>Does not provide emergency medical guidance</li>
                    </ul>
                </section>

                <section className="about-section">
                    <h2><Code size={24} /> Technology Stack</h2>
                    <div className="tech-grid">
                        <div className="tech-item">
                            <strong>Frontend</strong>
                            <span>React + Vite</span>
                        </div>
                        <div className="tech-item">
                            <strong>Backend</strong>
                            <span>FastAPI + Python</span>
                        </div>
                        <div className="tech-item">
                            <strong>ML</strong>
                            <span>scikit-learn, PyTorch</span>
                        </div>
                        <div className="tech-item">
                            <strong>Explainability</strong>
                            <span>SHAP</span>
                        </div>
                    </div>
                </section>

                <section className="about-section">
                    <h2><CheckCircle size={24} /> Model Information</h2>
                    <p>
                        Our models are trained on publicly available medical datasets with proper
                        validation methodology:
                    </p>
                    <ul>
                        <li>Stratified train/test splits</li>
                        <li>Cross-validation for reliable metrics</li>
                        <li>Probability calibration for honest confidence estimates</li>
                        <li>Optimized for recall (minimizing false negatives)</li>
                    </ul>
                    <p className="disclaimer-text">
                        Reported accuracies reflect honest evaluation metrics, not inflated claims.
                        Medical screening tools prioritize sensitivity over specificity to minimize
                        missed cases.
                    </p>
                </section>
            </div>

            <div className="about-footer">
                <p>
                    <strong>Disclaimer:</strong> This software is provided "as is" for educational
                    purposes. The developers are not liable for any decisions made based on the
                    outputs of this system. Always consult qualified healthcare professionals
                    for medical advice.
                </p>
            </div>
        </div>
    )
}

export default About
