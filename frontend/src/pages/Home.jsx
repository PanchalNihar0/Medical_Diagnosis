import { Link } from 'react-router-dom'
import {
    Activity, Heart, Droplets, FlaskConical, Ribbon, Bug, Wind,
    ArrowRight, Shield, Brain, FileText, TrendingUp
} from 'lucide-react'
import './Home.css'

const diseases = [
    {
        id: 'diabetes',
        name: 'Diabetes',
        description: 'Assess type 2 diabetes risk based on glucose, BMI, and other factors',
        icon: Activity,
        color: '#3b82f6',
        inputType: 'Clinical values'
    },
    {
        id: 'heart',
        name: 'Heart Disease',
        description: 'Evaluate cardiovascular disease risk factors',
        icon: Heart,
        color: '#ef4444',
        inputType: 'Clinical values'
    },
    {
        id: 'kidney',
        name: 'Kidney Disease',
        description: 'Screen for chronic kidney disease indicators',
        icon: Droplets,
        color: '#8b5cf6',
        inputType: 'Lab values'
    },
    {
        id: 'liver',
        name: 'Liver Disease',
        description: 'Assess liver function and disease risk',
        icon: FlaskConical,
        color: '#10b981',
        inputType: 'Lab values'
    },
    {
        id: 'breast-cancer',
        name: 'Breast Cancer',
        description: 'Analyze tumor characteristics for malignancy assessment',
        icon: Ribbon,
        color: '#ec4899',
        inputType: 'Biopsy data'
    },
    {
        id: 'malaria',
        name: 'Malaria',
        description: 'Detect malaria parasites from blood smear images',
        icon: Bug,
        color: '#f59e0b',
        inputType: 'Cell image'
    },
    {
        id: 'pneumonia',
        name: 'Pneumonia',
        description: 'Analyze chest X-rays for pneumonia indicators',
        icon: Wind,
        color: '#06b6d4',
        inputType: 'X-ray image'
    }
]

const features = [
    {
        icon: Brain,
        title: 'AI-Powered Analysis',
        description: 'Machine learning models trained on validated medical datasets'
    },
    {
        icon: Shield,
        title: 'Confidence Scoring',
        description: 'Transparent confidence levels for every prediction'
    },
    {
        icon: TrendingUp,
        title: 'What-If Analysis',
        description: 'See how changing factors affects your risk assessment'
    },
    {
        icon: FileText,
        title: 'PDF Reports',
        description: 'Download detailed reports to share with your doctor'
    }
]

function Home() {
    return (
        <div className="home">
            {/* Hero Section */}
            <section className="hero">
                <div className="container">
                    <div className="hero-content">
                        <div className="hero-badge">
                            <Shield size={16} />
                            <span>AI-Powered Health Screening</span>
                        </div>
                        <h1 className="hero-title">
                            Understand Your<br />
                            <span className="gradient-text">Health Risks</span>
                        </h1>
                        <p className="hero-description">
                            Get AI-powered risk assessments for common health conditions.
                            Our models provide transparent, explainable predictions to help
                            you have informed conversations with healthcare providers.
                        </p>
                        <div className="hero-actions">
                            <Link to="/diabetes" className="btn btn-primary btn-lg">
                                Start Assessment
                                <ArrowRight size={20} />
                            </Link>
                            <Link to="/about" className="btn btn-outline btn-lg">
                                Learn More
                            </Link>
                        </div>
                    </div>
                    <div className="hero-visual">
                        <div className="hero-card">
                            <div className="hero-card-header">
                                <Activity size={24} />
                                <span>Sample Assessment</span>
                            </div>
                            <div className="hero-card-body">
                                <div className="confidence-demo">
                                    <div className="confidence-bar" style={{ '--level': '72%' }}></div>
                                </div>
                                <p className="hero-card-text">72% confidence - Medium Risk</p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Disease Cards */}
            <section className="diseases-section">
                <div className="container">
                    <div className="section-header">
                        <h2>Health Assessments</h2>
                        <p>Select a condition to begin your risk assessment</p>
                    </div>
                    <div className="diseases-grid">
                        {diseases.map(disease => (
                            <Link
                                key={disease.id}
                                to={`/${disease.id}`}
                                className="disease-card"
                                style={{ '--accent-color': disease.color }}
                            >
                                <div className="disease-icon">
                                    <disease.icon size={28} />
                                </div>
                                <div className="disease-content">
                                    <h3>{disease.name}</h3>
                                    <p>{disease.description}</p>
                                    <div className="disease-meta">
                                        <span className="disease-input-type">{disease.inputType}</span>
                                        <ArrowRight size={16} className="disease-arrow" />
                                    </div>
                                </div>
                            </Link>
                        ))}
                    </div>
                </div>
            </section>

            {/* Features Section */}
            <section className="features-section">
                <div className="container">
                    <div className="section-header">
                        <h2>How It Works</h2>
                        <p>Transparent, explainable AI for better health decisions</p>
                    </div>
                    <div className="features-grid">
                        {features.map((feature, index) => (
                            <div key={index} className="feature-card">
                                <div className="feature-icon">
                                    <feature.icon size={24} />
                                </div>
                                <h3>{feature.title}</h3>
                                <p>{feature.description}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="cta-section">
                <div className="container">
                    <div className="cta-card">
                        <h2>Ready to assess your health risks?</h2>
                        <p>
                            Start with any of our screening tools. Remember, these are
                            educational tools—always consult healthcare professionals
                            for medical advice.
                        </p>
                        <Link to="/diabetes" className="btn btn-primary btn-lg">
                            Begin Assessment
                            <ArrowRight size={20} />
                        </Link>
                    </div>
                </div>
            </section>
        </div>
    )
}

export default Home
