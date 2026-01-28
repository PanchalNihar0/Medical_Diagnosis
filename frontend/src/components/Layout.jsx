import { Outlet, Link, useLocation } from 'react-router-dom'
import {
    Activity, Heart, Droplets, FlaskConical, Ribbon, Bug,
    Wind, Home, Info, AlertTriangle
} from 'lucide-react'
import './Layout.css'

const navItems = [
    { path: '/', label: 'Home', icon: Home },
    { path: '/diabetes', label: 'Diabetes', icon: Activity },
    { path: '/heart', label: 'Heart', icon: Heart },
    { path: '/kidney', label: 'Kidney', icon: Droplets },
    { path: '/liver', label: 'Liver', icon: FlaskConical },
    { path: '/breast-cancer', label: 'Breast Cancer', icon: Ribbon },
    { path: '/malaria', label: 'Malaria', icon: Bug },
    { path: '/pneumonia', label: 'Pneumonia', icon: Wind },
]

function Layout() {
    const location = useLocation()

    return (
        <div className="layout">
            {/* Disclaimer Banner */}
            <div className="disclaimer-banner">
                <AlertTriangle size={16} />
                <span>
                    <strong>Screening Tool Only:</strong> This system provides risk assessments,
                    not medical diagnoses. Always consult healthcare professionals.
                </span>
            </div>

            {/* Header */}
            <header className="header">
                <div className="container">
                    <Link to="/" className="logo">
                        <div className="logo-icon">
                            <Activity size={28} />
                        </div>
                        <div className="logo-text">
                            <span className="logo-title">MediScreen</span>
                            <span className="logo-subtitle">AI Health Risk Assessment</span>
                        </div>
                    </Link>

                    <nav className="nav">
                        {navItems.slice(0, 5).map(item => (
                            <Link
                                key={item.path}
                                to={item.path}
                                className={`nav-link ${location.pathname === item.path ? 'active' : ''}`}
                            >
                                <item.icon size={18} />
                                <span>{item.label}</span>
                            </Link>
                        ))}
                        <div className="nav-more">
                            <button className="nav-link">More ▾</button>
                            <div className="nav-dropdown">
                                {navItems.slice(5).map(item => (
                                    <Link key={item.path} to={item.path} className="nav-dropdown-item">
                                        <item.icon size={16} />
                                        <span>{item.label}</span>
                                    </Link>
                                ))}
                                <Link to="/about" className="nav-dropdown-item">
                                    <Info size={16} />
                                    <span>About</span>
                                </Link>
                            </div>
                        </div>
                    </nav>
                </div>
            </header>

            {/* Main Content */}
            <main className="main">
                <Outlet />
            </main>

            {/* Footer */}
            <footer className="footer">
                <div className="container">
                    <div className="footer-content">
                        <div className="footer-brand">
                            <Activity size={20} />
                            <span>MediScreen</span>
                        </div>
                        <p className="footer-disclaimer">
                            This tool is for educational and screening purposes only.
                            Results are not medical diagnoses. Always seek professional medical advice.
                        </p>
                        <div className="footer-links">
                            <Link to="/about">About</Link>
                            <a href="https://github.com" target="_blank" rel="noopener noreferrer">GitHub</a>
                        </div>
                    </div>
                </div>
            </footer>
        </div>
    )
}

export default Layout
