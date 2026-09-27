import React, { useState, useEffect } from 'react';
import { 
  Settings as SettingsIcon, 
  ShieldCheck, 
  Cpu, 
  Database, 
  Server, 
  Radio, 
  ExternalLink,
  Zap,
  CheckCircle2
} from 'lucide-react';
import axios from 'axios';
import { runSimulation } from '../services/api';

export default function Settings() {
  const [health, setHealth] = useState(null);
  const [seeding, setSeeding] = useState(false);
  const [seedMsg, setSeedMsg] = useState(null);

  useEffect(() => {
    axios.get('/health')
      .then(res => setHealth(res.data))
      .catch(() => setHealth({ status: 'offline', database: 'disconnected', llm_provider: 'unknown' }));
  }, []);

  const handleSeedAttack = async () => {
    setSeeding(true);
    setSeedMsg(null);
    try {
      const res = await runSimulation('admin_discovery');
      setSeedMsg(`Simulated campaign executed! Attacker session: ${res.session_id.substring(0, 8)}`);
    } catch (e) {
      setSeedMsg(`Failed to run campaign: ${e.message}`);
    } finally {
      setSeeding(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div>
        <h1 style={{ fontSize: '24px', fontWeight: '700', color: '#f8fafc' }}>System Configuration & Status</h1>
        <p style={{ color: '#94a3b8', fontSize: '14px', marginTop: '4px' }}>
          Deception engine parameters, safety boundaries, and live service health diagnostics.
        </p>
      </div>

      {seedMsg && (
        <div style={{ padding: '12px 16px', background: 'rgba(56, 189, 248, 0.15)', border: '1px solid #38bdf8', color: '#38bdf8', borderRadius: '8px', fontSize: '14px' }}>
          {seedMsg}
        </div>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '20px' }}>
        {/* Core System Status */}
        <div className="glass-card" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', color: '#38bdf8', marginBottom: '16px' }}>
            <Server style={{ width: '20px', height: '20px' }} />
            <h3 style={{ fontSize: '16px', color: '#f8fafc' }}>Engine Health & Gateways</h3>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', fontSize: '13px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 0', borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
              <span style={{ color: '#94a3b8' }}>Backend SOC Core:</span>
              <span style={{ color: '#10b981', fontWeight: '600', display: 'flex', alignItems: 'center', gap: '6px' }}>
                <CheckCircle2 style={{ width: '14px', height: '14px' }} /> {health?.status === 'healthy' ? 'ONLINE (Port 8000)' : 'CHECKING...'}
              </span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 0', borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
              <span style={{ color: '#94a3b8' }}>Deception Gateway:</span>
              <a
                href="http://127.0.0.1:8000/gateway/"
                target="_blank"
                rel="noreferrer"
                style={{ color: '#38bdf8', fontWeight: '600', textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '4px' }}
              >
                http://127.0.0.1:8000/gateway/ <ExternalLink style={{ width: '12px', height: '12px' }} />
              </a>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 0', borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
              <span style={{ color: '#94a3b8' }}>Database Backend:</span>
              <span style={{ color: '#10b981', fontWeight: '600' }}>SQLite (deception.db)</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 0' }}>
              <span style={{ color: '#94a3b8' }}>Simulated Company:</span>
              <span style={{ color: '#f8fafc' }}>Meridian Technologies Ltd.</span>
            </div>
          </div>
        </div>

        {/* LLM Engine */}
        <div className="glass-card" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', color: '#a855f7', marginBottom: '16px' }}>
            <Cpu style={{ width: '20px', height: '20px' }} />
            <h3 style={{ fontSize: '16px', color: '#f8fafc' }}>LLM Synthesis Engine</h3>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', fontSize: '13px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 0', borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
              <span style={{ color: '#94a3b8' }}>Active Provider:</span>
              <span style={{ color: '#10b981', fontWeight: '600', textTransform: 'capitalize' }}>
                {health?.llm_provider || 'Mock'} Provider (Zero-Risk)
              </span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 0', borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
              <span style={{ color: '#94a3b8' }}>Ollama Local Model:</span>
              <span style={{ color: '#f8fafc' }}>http://localhost:11434 (llama3)</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 0', borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
              <span style={{ color: '#94a3b8' }}>OpenAI Integration:</span>
              <span style={{ color: '#94a3b8' }}>Configurable via .env</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 0' }}>
              <span style={{ color: '#94a3b8' }}>Automatic Fallback:</span>
              <span style={{ color: '#10b981' }}>Enabled (Mock Synthesis)</span>
            </div>
          </div>
        </div>

        {/* Safety Guardrails */}
        <div className="glass-card" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', color: '#10b981', marginBottom: '16px' }}>
            <ShieldCheck style={{ width: '20px', height: '20px' }} />
            <h3 style={{ fontSize: '16px', color: '#f8fafc' }}>Security & Safety Guardrails</h3>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', fontSize: '13px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 0', borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
              <span style={{ color: '#94a3b8' }}>Synthetic Marker Enforced:</span>
              <span style={{ color: '#10b981', fontWeight: '600' }}>ACTIVE (is_synthetic = True)</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 0', borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
              <span style={{ color: '#94a3b8' }}>Prohibited Commands Filter:</span>
              <span style={{ color: '#10b981' }}>Enforced (LureValidator)</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 0' }}>
              <span style={{ color: '#94a3b8' }}>Trigger Risk Score Threshold:</span>
              <span className="mono" style={{ color: '#f8fafc', fontWeight: '700' }}>Score &ge; 4.0</span>
            </div>
          </div>
        </div>

        {/* Quick Operations */}
        <div className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', color: '#f59e0b', marginBottom: '16px' }}>
              <Zap style={{ width: '20px', height: '20px' }} />
              <h3 style={{ fontSize: '16px', color: '#f8fafc' }}>Diagnostic Operations</h3>
            </div>
            <p style={{ color: '#94a3b8', fontSize: '13px' }}>
              Trigger an instant synthetic adversary attack scenario against the portal to test detection, stage escalation, and lure engagement.
            </p>
          </div>
          <button
            disabled={seeding}
            onClick={handleSeedAttack}
            style={{
              padding: '12px 18px',
              borderRadius: '8px',
              background: 'linear-gradient(135deg, #0284c7, #38bdf8)',
              color: 'white',
              border: 'none',
              fontWeight: '600',
              fontSize: '13px',
              cursor: seeding ? 'not-allowed' : 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '8px',
              marginTop: '20px'
            }}
          >
            <Zap style={{ width: '15px', height: '15px' }} />
            {seeding ? 'Running Diagnostic Attack...' : 'Trigger Diagnostic Attack Sequence'}
          </button>
        </div>
      </div>
    </div>
  );
}
