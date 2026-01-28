import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Home from './pages/Home'
import DiabetesPredictor from './pages/DiabetesPredictor'
import HeartPredictor from './pages/HeartPredictor'
import KidneyPredictor from './pages/KidneyPredictor'
import LiverPredictor from './pages/LiverPredictor'
import BreastCancerPredictor from './pages/BreastCancerPredictor'
import MalariaPredictor from './pages/MalariaPredictor'
import PneumoniaPredictor from './pages/PneumoniaPredictor'
import About from './pages/About'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="diabetes" element={<DiabetesPredictor />} />
        <Route path="heart" element={<HeartPredictor />} />
        <Route path="kidney" element={<KidneyPredictor />} />
        <Route path="liver" element={<LiverPredictor />} />
        <Route path="breast-cancer" element={<BreastCancerPredictor />} />
        <Route path="malaria" element={<MalariaPredictor />} />
        <Route path="pneumonia" element={<PneumoniaPredictor />} />
        <Route path="about" element={<About />} />
      </Route>
    </Routes>
  )
}

export default App
