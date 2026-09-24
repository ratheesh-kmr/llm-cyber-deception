import React, { useState, useEffect } from 'react';
import { Play, CheckCircle, AlertTriangle, Loader2 } from 'lucide-react';
import { getSimulationScenarios, runSimulation } from '../services/api';

export default function Simulation({ onRefresh }) {
  const [scenarios, setScenarios] = useState([]);
  const [running, setRunning] = useState(null);
  const [results, setResults] = useState({});

  useEffect(() => {
    getSimulationScenarios().then(setScenarios).catch(console.error);
  }, []);

  const handleRun = async (scenarioId) => {
    setRunning(scenarioId);
    try {
      const res = await runSimulation(scenarioId);
      setResults((prev) => ({ ...prev, [scenarioId]: res }));
      onRefresh();
    } catch (e) {
      setResults((prev) => ({ ...prev, [scenarioId]: { status: 'failed', error: e.message } }));
    } finally {
      setRunning(null);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div>
        <h1 style={{ fontSize: '24px', fontWeight: '700', color: '#f8fafc' }}>Attack Simulator</h1>
        <p style={{ color: '#94a3b8', fontSize: '14px', marginTop: '4px' }}>
          Execute safe, deterministic HTTP request sequences against the deception gateway to evaluate threat scoring & lure generation.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '20px' }}>
        {scenarios.map((sc) => {
          const res = results[sc.scenario_id];
          const isRunning = running === sc.scenario_id;

          return (
            <div key={sc.scenario_id} className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                  <h3 style={{ fontSize: '18px', color: '#f8fafc' }}>{sc.name}</h3>
                  <span style={{ fontSize: '11px', background: 'rgba(56, 189, 248, 0.15)', color: '#38bdf8', padding: '3px 8px', borderRadius: '4px', fontWeight: '600' }}>
                    {sc.step_count} STEPS
                  </span>
                </div>
                <p style={{ color: '#94a3b8', fontSize: '13px', marginTop: '8px', marginBottom: '16px' }}>
                  {sc.description}
                </p>
                <div style={{ fontSize: '12px', color: '#64748b' }}>
                  Target Interest: <strong style={{ color: '#e2e8f0' }}>{sc.expected_interest}</strong> | Target Stage: <strong style={{ color: '#e2e8f0' }}>{sc.expected_stage}</strong>
                </div>
              </div>

              <div style={{ marginTop: '20px', borderTop: '1px solid rgba(255,255,255,0.06)', paddingTop: '16px' }}>
                {res && (
                  <div style={{
                    padding: '12px',
                    borderRadius: '6px',
                    marginBottom: '12px',
                    background: res.status === 'completed' ? 'rgba(16, 185, 129, 0.15)' : 'rgba(239, 68, 68, 0.15)',
                    border: `1px solid ${res.status === 'completed' ? 'rgba(16, 185, 129, 0.3)' : 'rgba(239, 68, 68, 0.3)'}`,
                    fontSize: '12px'
                  }}>
                    {res.status === 'completed' ? (
                      <div style={{ color: '#10b981' }}>
                        ✔ Completed successfully! Session: <span className="mono">{res.session_id.substring(0, 8)}</span> | Final Risk Score: <strong>{res.final_risk_score}</strong>
                      </div>
                    ) : (
                      <div style={{ color: '#f87171' }}>✖ Error: {res.error}</div>
                    )}
                  </div>
                )}

                <button
                  disabled={isRunning}
                  onClick={() => handleRun(sc.scenario_id)}
                  style={{
                    width: '100%',
                    padding: '10px 16px',
                    borderRadius: '6px',
                    background: isRunning ? '#334155' : 'linear-gradient(135deg, #0284c7, #38bdf8)',
                    color: 'white',
                    border: 'none',
                    fontWeight: '600',
                    fontSize: '13px',
                    cursor: isRunning ? 'not-allowed' : 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: '8px'
                  }}
                >
                  {isRunning ? <Loader2 style={{ width: '16px', height: '16px', animation: 'spin 1s linear infinite' }} /> : <Play style={{ width: '16px', height: '16px' }} />}
                  {isRunning ? 'Executing Scenario...' : 'Execute Simulation'}
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
