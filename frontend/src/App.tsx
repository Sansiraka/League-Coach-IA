// Define y provee el enrutamiento principal de la aplicación
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Sidebar } from './components/Sidebar';
import { DashboardOverview } from './pages/DashboardOverview';
import { MatchHistory } from './pages/MatchHistory';
import { AiAnalysis } from './pages/AiAnalysis';
import { Settings } from './pages/Settings';
import { PlayerProvider } from './context/PlayerContext';

function App() {
  return (
    <PlayerProvider>
      <Router>
        <div className="min-h-screen bg-coach-dark flex text-coach-text">
          <Sidebar />
          
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<DashboardOverview />} />
            <Route path="/matches" element={<MatchHistory />} />
            <Route path="/analysis" element={<AiAnalysis />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </div>
      </Router>
    </PlayerProvider>
  );
}

export default App;
