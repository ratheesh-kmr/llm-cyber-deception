import React from 'react';
import { Target, CheckCircle } from 'lucide-react';

export default function Interactions({ interactions }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div>
        <h1 style={{ fontSize: '24px', fontWeight: '700', color: '#f8fafc' }}>Lure Engagement Log</h1>
        <p style={{ color: '#94a3b8', fontSize: '14px', marginTop: '4px' }}>
          Audit records of attackers trapped by deployed LLM lures, confirming deception effectiveness.
        </p>
      </div>

      <div className="glass-card" style={{ padding: '24px' }}>
        <table>
          <thead>
            <tr>
              <th>Interaction ID</th>
              <th>Timestamp</th>
              <th>Lure ID</th>
              <th>Session ID</th>
              <th>Action Type</th>
              <th>Engagement Status</th>
            </tr>
          </thead>
          <tbody>
            {(interactions || []).map((item) => (
              <tr key={item.id}>
                <td className="mono" style={{ color: '#94a3b8' }}>#{item.id}</td>
                <td className="mono" style={{ fontSize: '12px' }}>{new Date(item.timestamp).toLocaleTimeString()}</td>
                <td className="mono" style={{ color: '#a855f7' }}>{item.lure_id.substring(0, 8)}...</td>
                <td className="mono" style={{ color: '#38bdf8' }}>{item.session_id.substring(0, 8)}...</td>
                <td>
                  <span style={{
                    background: 'rgba(16, 185, 129, 0.15)',
                    color: '#10b981',
                    padding: '4px 10px',
                    borderRadius: '4px',
                    fontSize: '12px',
                    fontWeight: '600'
                  }}>
                    {item.interaction_type}
                  </span>
                </td>
                <td style={{ color: '#10b981', display: 'flex', alignItems: 'center', gap: '6px', fontSize: '13px' }}>
                  <CheckCircle style={{ width: '15px', height: '15px' }} /> Trapped & Logged
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
