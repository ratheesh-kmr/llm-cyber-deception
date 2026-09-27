import React, { useState } from 'react';
import RiskBadge from '../components/RiskBadge';
import { generateLure, getSessionDetail } from '../services/api';
import { 
  Sparkles, 
  Search, 
  Filter, 
  Eye, 
  X, 
  Clock, 
  ShieldAlert, 
  Crosshair, 
  ArrowRight,
  Terminal,
  Activity
} from 'lucide-react';

const STAGES = [
  'RECONNAISSANCE',
  'RESOURCE_DISCOVERY',
  'CONFIGURATION_DISCOVERY',
  'CREDENTIAL_DISCOVERY',
  'LURE_INTERACTION',
  'CREDENTIAL_ATTEMPT'
];

export default function Sessions({ sessions, onRefresh }) {
  const [generating, setGenerating] = useState(null);
  const [msg, setMsg] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedSession, setSelectedSession] = useState(null);
  const [sessionDetail, setSessionDetail] = useState(null);
  const [loadingDetail, setLoadingDetail] = useState(false);

  const handleGenLure = async (sessionId, interest) => {
    setGenerating(sessionId);
    try {
      await generateLure(sessionId, interest);
      setMsg(`Lure generated & deployed for session ${sessionId.substring(0, 8)}`);
      onRefresh();
      if (selectedSession === sessionId) {
        openSessionDetail(sessionId);
      }
    } catch (e) {
      setMsg(`Failed to generate lure: ${e.message}`);
    } finally {
      setGenerating(null);
    }
  };

  const openSessionDetail = async (sessionId) => {
    setSelectedSession(sessionId);
    setLoadingDetail(true);
    try {
      const detail = await getSessionDetail(sessionId);
      setSessionDetail(detail);
    } catch (err) {
      console.error("Failed to load session details", err);
    } finally {
      setLoadingDetail(false);
    }
  };

  const filteredSessions = (sessions || []).filter(s => {
    const term = searchTerm.toLowerCase();
    return s.session_id.toLowerCase().includes(term) ||
      s.source_ip.toLowerCase().includes(term) ||
      (s.behavior_type && s.behavior_type.toLowerCase().includes(term));
  });

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <h1 style={{ fontSize: '24px', fontWeight: '700', color: '#f8fafc' }}>Attacker Sessions</h1>
          <p style={{ color: '#94a3b8', fontSize: '14px', marginTop: '4px' }}>
            Live adversary tracking, automated attack stage profiling, and targeted deception deployment.
          </p>
        </div>

        {/* Search & Filter */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            background: 'rgba(30, 41, 59, 0.6)',
            padding: '8px 14px',
            borderRadius: '8px',
            border: '1px solid var(--border-color)'
          }}>
            <Search style={{ width: '16px', height: '16px', color: '#64748b' }} />
            <input
              type="text"
              placeholder="Search IP, Session ID, or Target..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              style={{
                background: 'transparent',
                border: 'none',
                color: '#f8fafc',
                fontSize: '13px',
                outline: 'none',
                width: '240px'
              }}
            />
          </div>
        </div>
      </div>

      {msg && (
        <div style={{ padding: '12px 16px', background: 'rgba(56, 189, 248, 0.15)', border: '1px solid #38bdf8', color: '#38bdf8', borderRadius: '8px', fontSize: '14px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span>{msg}</span>
          <button onClick={() => setMsg(null)} style={{ background: 'none', border: 'none', color: '#38bdf8', cursor: 'pointer' }}>✕</button>
        </div>
      )}

      {/* Main Sessions Table */}
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
              <th style={{ textAlign: 'right' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredSessions.map((s) => (
              <tr 
                key={s.session_id} 
                onClick={() => openSessionDetail(s.session_id)}
                style={{ cursor: 'pointer', transition: 'background 0.2s' }}
              >
                <td className="mono" style={{ color: '#38bdf8', fontWeight: '600' }}>
                  {s.session_id.substring(0, 12)}...
                </td>
                <td className="mono">{s.source_ip}</td>
                <td className="mono" style={{ fontSize: '12px', color: '#94a3b8' }}>
                  {new Date(s.first_seen).toLocaleTimeString()}
                </td>
                <td className="mono" style={{ fontSize: '12px', color: '#94a3b8' }}>
                  {new Date(s.last_seen).toLocaleTimeString()}
                </td>
                <td>
                  <span style={{
                    background: 'rgba(168, 85, 247, 0.15)',
                    padding: '4px 10px',
                    borderRadius: '4px',
                    fontSize: '12px',
                    color: '#c084fc',
                    fontWeight: '600'
                  }}>
                    {s.behavior_type || 'RECONNAISSANCE'}
                  </span>
                </td>
                <td className="mono" style={{ fontWeight: '700', fontSize: '15px' }}>
                  {s.risk_score.toFixed(1)}
                </td>
                <td>
                  <RiskBadge level={s.risk_score >= 11 ? 'CRITICAL' : s.risk_score >= 7 ? 'HIGH' : s.risk_score >= 3 ? 'MEDIUM' : 'LOW'} />
                </td>
                <td style={{ textAlign: 'right' }}>
                  <div style={{ display: 'inline-flex', gap: '8px' }} onClick={(e) => e.stopPropagation()}>
                    <button
                      onClick={() => openSessionDetail(s.session_id)}
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '6px',
                        padding: '6px 12px',
                        borderRadius: '6px',
                        background: 'rgba(56, 189, 248, 0.15)',
                        border: '1px solid rgba(56, 189, 248, 0.3)',
                        color: '#38bdf8',
                        fontSize: '12px',
                        fontWeight: '600',
                        cursor: 'pointer'
                      }}
                    >
                      <Eye style={{ width: '13px', height: '13px' }} />
                      Investigate
                    </button>
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
                      {generating === s.session_id ? 'Generating...' : 'Deploy Lure'}
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Session Investigation Modal */}
      {selectedSession && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          width: '100vw',
          height: '100vh',
          background: 'rgba(0, 0, 0, 0.75)',
          backdropFilter: 'blur(8px)',
          display: 'flex',
          justifyContent: 'flex-end',
          zIndex: 100
        }}>
          <div style={{
            width: '680px',
            height: '100vh',
            background: '#0d131f',
            borderLeft: '1px solid var(--border-color)',
            display: 'flex',
            flexDirection: 'column',
            overflowY: 'auto',
            padding: '32px',
            gap: '24px',
            boxShadow: '-10px 0 40px rgba(0,0,0,0.5)'
          }}>
            {/* Header */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#38bdf8', fontSize: '12px', fontWeight: '700' }}>
                  <Activity style={{ width: '16px', height: '16px' }} /> SESSION FORENSICS & TIMELINE
                </div>
                <h2 className="mono" style={{ fontSize: '20px', color: '#f8fafc', marginTop: '4px' }}>
                  {selectedSession}
                </h2>
              </div>
              <button
                onClick={() => { setSelectedSession(null); setSessionDetail(null); }}
                style={{
                  background: 'rgba(255,255,255,0.05)',
                  border: 'none',
                  borderRadius: '50%',
                  width: '36px',
                  height: '36px',
                  color: '#94a3b8',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center'
                }}
              >
                <X style={{ width: '20px', height: '20px' }} />
              </button>
            </div>

            {loadingDetail ? (
              <div style={{ padding: '60px', textAlign: 'center', color: '#94a3b8' }}>Loading session timeline & forensics...</div>
            ) : sessionDetail ? (
              <>
                {/* Attacker Overview Card */}
                <div style={{
                  display: 'grid',
                  gridTemplateColumns: 'repeat(3, 1fr)',
                  gap: '12px',
                  background: 'rgba(30, 41, 59, 0.5)',
                  padding: '16px',
                  borderRadius: '10px',
                  border: '1px solid var(--border-color)'
                }}>
                  <div>
                    <span style={{ fontSize: '11px', color: '#94a3b8' }}>SOURCE IP</span>
                    <div className="mono" style={{ fontSize: '14px', color: '#f8fafc', fontWeight: '600', marginTop: '4px' }}>
                      {sessionDetail.source_ip}
                    </div>
                  </div>
                  <div>
                    <span style={{ fontSize: '11px', color: '#94a3b8' }}>RISK SCORE</span>
                    <div className="mono" style={{ fontSize: '16px', color: '#f43f5e', fontWeight: '700', marginTop: '2px' }}>
                      {sessionDetail.risk_score.toFixed(1)}
                    </div>
                  </div>
                  <div>
                    <span style={{ fontSize: '11px', color: '#94a3b8' }}>TARGET PROFILE</span>
                    <div style={{ fontSize: '13px', color: '#a855f7', fontWeight: '600', marginTop: '4px' }}>
                      {sessionDetail.behavior_type || 'RECONNAISSANCE'}
                    </div>
                  </div>
                </div>

                {/* Attack Progression Stepper */}
                <div style={{ background: 'rgba(15, 23, 42, 0.6)', padding: '20px', borderRadius: '10px', border: '1px solid var(--border-color)' }}>
                  <h4 style={{ fontSize: '13px', color: '#94a3b8', marginBottom: '14px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
                    Attack Stage Progression
                  </h4>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                    {STAGES.map((st, idx) => {
                      const currentStage = sessionDetail.attack_sessions?.[0]?.attack_stage || 'RECONNAISSANCE';
                      const currentIdx = STAGES.indexOf(currentStage);
                      const isCompleted = idx <= currentIdx;
                      const isCurrent = idx === currentIdx;

                      return (
                        <div
                          key={st}
                          style={{
                            display: 'flex',
                            alignItems: 'center',
                            gap: '12px',
                            padding: '8px 12px',
                            borderRadius: '6px',
                            background: isCurrent ? 'rgba(56, 189, 248, 0.15)' : isCompleted ? 'rgba(16, 185, 129, 0.08)' : 'rgba(255, 255, 255, 0.02)',
                            border: isCurrent ? '1px solid #38bdf8' : '1px solid transparent'
                          }}
                        >
                          <div style={{
                            width: '20px',
                            height: '20px',
                            borderRadius: '50%',
                            background: isCurrent ? '#38bdf8' : isCompleted ? '#10b981' : '#334155',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            fontSize: '11px',
                            fontWeight: 'bold',
                            color: 'white'
                          }}>
                            {idx + 1}
                          </div>
                          <span style={{ fontSize: '12px', fontWeight: isCurrent ? '700' : '500', color: isCurrent ? '#38bdf8' : isCompleted ? '#e2e8f0' : '#64748b' }}>
                            {st.replace(/_/g, ' ')}
                          </span>
                          {isCurrent && (
                            <span style={{ marginLeft: 'auto', fontSize: '10px', padding: '2px 8px', borderRadius: '10px', background: '#38bdf8', color: '#090d16', fontWeight: 'bold' }}>
                              ACTIVE STAGE
                            </span>
                          )}
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* Event Stream Timeline */}
                <div>
                  <h4 style={{ fontSize: '13px', color: '#94a3b8', marginBottom: '14px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
                    Event Telemetry Timeline ({(sessionDetail.events || []).length} Events)
                  </h4>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                    {(sessionDetail.events || []).map((ev) => (
                      <div
                        key={ev.id}
                        style={{
                          background: 'rgba(30, 41, 59, 0.4)',
                          padding: '12px 16px',
                          borderRadius: '8px',
                          border: '1px solid rgba(255, 255, 255, 0.05)',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'space-between'
                        }}
                      >
                        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                          <span className="mono" style={{
                            fontSize: '11px',
                            fontWeight: '700',
                            padding: '3px 6px',
                            borderRadius: '4px',
                            background: ev.method === 'POST' ? 'rgba(239, 68, 68, 0.2)' : 'rgba(56, 189, 248, 0.2)',
                            color: ev.method === 'POST' ? '#f87171' : '#38bdf8'
                          }}>
                            {ev.method}
                          </span>
                          <span className="mono" style={{ fontSize: '13px', color: '#f8fafc' }}>
                            {ev.endpoint}
                          </span>
                        </div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                          <RiskBadge level={ev.severity} />
                          <span className="mono" style={{ fontSize: '11px', color: '#94a3b8' }}>
                            {new Date(ev.timestamp).toLocaleTimeString()}
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </>
            ) : (
              <div style={{ color: '#ef4444' }}>Failed to load session details.</div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
