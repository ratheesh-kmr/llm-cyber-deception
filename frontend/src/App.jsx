import React, { useState, useEffect, useCallback } from 'react';
import Sidebar from './components/Sidebar';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import Sessions from './pages/Sessions';
import Events from './pages/Events';
import Lures from './pages/Lures';
import Interactions from './pages/Interactions';
import Simulation from './pages/Simulation';
import Settings from './pages/Settings';
import { 
  getDashboardSummary, 
  getSessions, 
  getEvents, 
  getLures, 
  getInteractions 
} from './services/api';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [summary, setSummary] = useState(null);
  const [sessions, setSessions] = useState([]);
  const [events, setEvents] = useState([]);
  const [lures, setLures] = useState([]);
  const [interactions, setInteractions] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchAllData = useCallback(async () => {
    try {
      const [sumData, sessData, evData, lureData, interData] = await Promise.all([
        getDashboardSummary().catch(() => null),
        getSessions().catch(() => []),
        getEvents().catch(() => []),
        getLures().catch(() => []),
        getInteractions().catch(() => [])
      ]);
      setSummary(sumData);
      setSessions(sessData);
      setEvents(evData);
      setLures(lureData);
      setInteractions(interData);
    } catch (err) {
      console.error("Error loading SOC platform data:", err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchAllData();
    const interval = setInterval(fetchAllData, 5000); // Auto refresh every 5s
    return () => clearInterval(interval);
  }, [fetchAllData]);

  return (
    <div style={{ display: 'flex', width: '100vw', minHeight: '100vh', background: 'var(--bg-primary)' }}>
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
      
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', minWidth: 0 }}>
        <Navbar onRefresh={fetchAllData} />
        
        <main style={{ flex: 1, padding: '32px', overflowY: 'auto' }}>
          {activeTab === 'dashboard' && (
            <Dashboard 
              summary={summary} 
              sessions={sessions} 
              onNavigate={setActiveTab} 
              onRunSimulation={() => setActiveTab('simulation')} 
            />
          )}
          {activeTab === 'sessions' && <Sessions sessions={sessions} onRefresh={fetchAllData} />}
          {activeTab === 'events' && <Events events={events} />}
          {activeTab === 'lures' && <Lures lures={lures} onRefresh={fetchAllData} />}
          {activeTab === 'interactions' && <Interactions interactions={interactions} />}
          {activeTab === 'simulation' && <Simulation onRefresh={fetchAllData} />}
          {activeTab === 'settings' && <Settings />}
        </main>
      </div>
    </div>
  );
}
