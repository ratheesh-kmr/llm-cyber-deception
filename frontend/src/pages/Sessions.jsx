import React, { useState } from 'react';
import RiskBadge from '../components/RiskBadge';
import { generateLure } from '../services/api';
import { Sparkles } from 'lucide-react';

export default function Sessions({ sessions, onRefresh }) {
  const [generating, setGenerating] = useState(null);
  const [msg, setMsg] = useState(null);

  const handleGenLure = async (sessionId, interest) => {
    setGenerating(sessionId);
    try {
      await generateLure(sessionId, interest);
      setMsg(`Lure generated & deployed for session ${sessionId.substring(0, 8)}`);
      onRefresh();
    } catch (e) {
      setMsg(`Failed to generate lure: ${e.message}`);
    } finally {
      setGenerating(null);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div>
        <h1 style={{ fontSize: '24px', fontWeight: '700', color: '#f8fafc' }}>Attacker Sessions</h1>
        <p style={{ color: '#94a3b8', fontSize: '14px', marginTop: '4px' }}>
          Identified adversary campaigns with real-time risk scores and target classification.
        </p>
      </div>

      {msg && (
        <div style={{ padding: '12px 16px', background: 'rgba(56, 189, 248, 0.15)', border: '1px solid #38bdf8', color: '#38bdf8', borderRadius: '8px', fontSize: '14px' }}>
          {msg}
        </div>
      )}

      <div className="glass-card" style={{ padding: '24px' }}>
        <table>
          <thead>
            <tr>
              <th>Session ID</th>
              <th>Source IP</th>
              <th>First Seen</th>
              <th>Last Seen</th>
              <th>Behavior Type</th>
              <th>Risk Score</th>
              <th>Risk Level</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {(sessions || []).map((s) => (
              <tr key={s.session_id}>
                <td className="mono" style={{ color: '#38bdf8' }}>{s.session_id}</td>
                <td className="mono">{s.source_ip}</td>
                <td className="mono" style={{ fontSize: '12px', color: '#94a3b8' }}>{new Date(s.first_seen).toLocaleTimeString()}</td>
                <td className="mono" style={{ fontSize: '12px', color: '#94a3b8' }}>{new Date(s.last_seen).toLocaleTimeString()}</td>
                <td>
                  <span style={{ background: 'rgba(255,255,255,0.06)', padding: '4px 8px', borderRadius: '4px', fontSize: '12px', color: '#a855f7', fontWeight: '600' }}>
                    {s.behavior_type || 'RECONNAISSANCE'}
                  </span>
                </td>
                <td className="mono" style={{ fontWeight: '700', fontSize: '15px' }}>{s.risk_score.toFixed(1)}</td>
                <td><RiskBadge level={s.risk_score >= 11 ? 'CRITICAL' : s.risk_score >= 7 ? 'HIGH' : s.risk_score >= 3 ? 'MEDIUM' : 'LOW'} /></td>
                <td>
                  <button
                    disabled={generating === s.session_id}
                    onClick={() => handleGenLure(s.session_id, (s.behavior_type || 'database').toLowerCase())}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '6px',
                      padding: '6px 12px',
                      borderRadius: '6px',
                      background: 'rgba(168, 85, 247, 0.2)',
                      border: '1px solid rgba(168, 85, 247, 0.4)',
                      color: '#c084fc',
                      fontSize: '12px',
                      fontWeight: '600',
                      cursor: 'pointer'
                    }}
                  >
                    <Sparkles style={{ width: '13px', height: '13px' }} />
                    {generating === s.session_id ? 'Generating...' : 'Trigger LLM Lure'}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
