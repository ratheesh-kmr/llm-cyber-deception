import React from 'react';
import { Activity, ShieldAlert, FileCode, Target, Play, Zap } from 'lucide-react';
import MetricCard from '../components/MetricCard';
import RiskBadge from '../components/RiskBadge';

export default function Dashboard({ summary, sessions, onNavigate, onRunSimulation }) {
  if (!summary) return <div style={{ padding: '40px', color: '#94a3b8' }}>Loading SOC dashboard metrics...</div>;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '28px' }}>
      <div>
        <h1 style={{ fontSize: '24px', fontWeight: '700', color: '#f8fafc' }}>Active SOC Operations</h1>
        <p style={{ color: '#94a3b8', fontSize: '14px', marginTop: '4px' }}>
          Real-time autonomous threat detection, risk evaluation, and dynamic LLM lure deployment engine.
        </p>
      </div>

      {/* Top Metrics Row */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '20px' }}>
        <MetricCard
          title="Active Attackers"
          value={summary.active_sessions}
          subtext={`${summary.total_sessions} total campaigns recorded`}
          icon={Activity}
          color="#38bdf8"
        />
        <MetricCard
          title="Critical Threats"
          value={summary.critical_sessions}
          subtext={`${summary.high_risk_sessions} high risk sessions`}
          icon={ShieldAlert}
          color="#f43f5e"
        />
        <MetricCard
          title="LLM Lures Deployed"
          value={summary.deployed_lures}
          subtext={`${summary.generated_lures} total lures in vault`}
          icon={FileCode}
          color="#a855f7"
        />
        <MetricCard
          title="Lure Engagement Rate"
          value={`${summary.lure_engagement_rate}%`}
          subtext={`${summary.lure_interactions} attacker interactions`}
          icon={Target}
          color="#10b981"
        />
      </div>

      {/* Main Grid: Attack Stage Distribution + Quick Simulator */}
      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '24px' }}>
        {/* Risk & Stage Overview */}
        <div className="glass-card" style={{ padding: '24px' }}>
          <h3 style={{ fontSize: '16px', color: '#f8fafc', marginBottom: '20px' }}>Attack Stage Distribution</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '16px' }}>
            {Object.entries(summary.attack_stage_distribution || {}).map(([stage, count]) => (
              <div key={stage} style={{
                background: 'rgba(30, 41, 59, 0.6)',
                padding: '16px',
                borderRadius: '8px',
                border: '1px solid var(--border-color)'
              }}>
                <span style={{ fontSize: '11px', color: '#94a3b8', fontWeight: '600' }}>{stage}</span>
                <div className="mono" style={{ fontSize: '22px', fontWeight: '700', color: '#38bdf8', marginTop: '6px' }}>
                  {count}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Simulator Launcher */}
        <div className="glass-card glow-cyan" style={{ padding: '24px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#38bdf8', fontSize: '12px', fontWeight: '700', textTransform: 'uppercase' }}>
              <Zap style={{ width: '16px', height: '16px' }} /> Quick Attack Simulator
            </div>
            <h3 style={{ fontSize: '18px', color: '#f8fafc', marginTop: '8px' }}>Launch Test Campaign</h3>
            <p style={{ color: '#94a3b8', fontSize: '13px', marginTop: '6px' }}>
              Trigger pre-scripted safe attack vectors to test risk scoring and LLM lure generation in real-time.
            </p>
          </div>
          <button
            onClick={() => onNavigate('simulation')}
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '10px',
              padding: '12px 20px',
              borderRadius: '8px',
              background: 'linear-gradient(135deg, #0284c7, #38bdf8)',
              color: 'white',
              border: 'none',
              fontWeight: '600',
              fontSize: '14px',
              cursor: 'pointer',
              marginTop: '20px'
            }}
          >
            <Play style={{ width: '16px', height: '16px' }} /> Launch Simulator Scenario
          </button>
        </div>
      </div>

      {/* Recent Sessions Table */}
      <div className="glass-card" style={{ padding: '24px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
          <h3 style={{ fontSize: '16px', color: '#f8fafc' }}>Recent Attacker Sessions</h3>
          <button
            onClick={() => onNavigate('sessions')}
            style={{ background: 'none', border: 'none', color: '#38bdf8', cursor: 'pointer', fontSize: '13px', fontWeight: '600' }}
          >
            View All &rarr;
          </button>
        </div>
        <table>
          <thead>
            <tr>
              <th>Session ID</th>
              <th>Source IP</th>
              <th>Target Interest</th>
              <th>Risk Score</th>
              <th>Risk Level</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {(sessions || []).slice(0, 5).map((session) => (
              <tr key={session.session_id}>
                <td className="mono" style={{ color: '#38bdf8' }}>{session.session_id.substring(0, 8)}...</td>
                <td className="mono">{session.source_ip}</td>
                <td><span style={{ background: 'rgba(255,255,255,0.06)', padding: '3px 8px', borderRadius: '4px', fontSize: '12px' }}>{session.behavior_type || 'RECON'}</span></td>
                <td className="mono" style={{ fontWeight: '700' }}>{session.risk_score.toFixed(1)}</td>
                <td><RiskBadge level={session.risk_score >= 11 ? 'CRITICAL' : session.risk_score >= 7 ? 'HIGH' : session.risk_score >= 3 ? 'MEDIUM' : 'LOW'} /></td>
                <td><span style={{ color: session.status === 'active' ? '#10b981' : '#94a3b8' }}>● {session.status}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
