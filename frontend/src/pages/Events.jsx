import React from 'react';
import RiskBadge from '../components/RiskBadge';

export default function Events({ events }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div>
        <h1 style={{ fontSize: '24px', fontWeight: '700', color: '#f8fafc' }}>Telemetry Events</h1>
        <p style={{ color: '#94a3b8', fontSize: '14px', marginTop: '4px' }}>
          Raw HTTP requests logged by the deception gateway with threat classification & risk deltas.
        </p>
      </div>

      <div className="glass-card" style={{ padding: '24px' }}>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Timestamp</th>
              <th>Session</th>
              <th>Method</th>
              <th>Endpoint</th>
              <th>Event Type</th>
              <th>Severity</th>
              <th>Risk Delta</th>
            </tr>
          </thead>
          <tbody>
            {(events || []).map((e) => (
              <tr key={e.id}>
                <td className="mono" style={{ color: '#94a3b8' }}>#{e.id}</td>
                <td className="mono" style={{ fontSize: '12px' }}>{new Date(e.timestamp).toLocaleTimeString()}</td>
                <td className="mono" style={{ color: '#38bdf8' }}>{e.session_id.substring(0, 8)}...</td>
                <td>
                  <span className="mono" style={{
                    padding: '3px 8px',
                    borderRadius: '4px',
                    fontWeight: '700',
                    fontSize: '11px',
                    background: e.method === 'POST' ? 'rgba(239, 68, 68, 0.2)' : 'rgba(56, 189, 248, 0.2)',
                    color: e.method === 'POST' ? '#f87171' : '#38bdf8'
                  }}>
                    {e.method}
                  </span>
                </td>
                <td className="mono" style={{ color: '#f3f4f6' }}>{e.endpoint}</td>
                <td><span style={{ color: '#94a3b8', fontSize: '12px' }}>{e.event_type}</span></td>
                <td><RiskBadge level={e.severity} /></td>
                <td className="mono" style={{ color: e.risk_delta > 0 ? '#f87171' : '#10b981', fontWeight: '700' }}>
                  +{e.risk_delta.toFixed(1)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
