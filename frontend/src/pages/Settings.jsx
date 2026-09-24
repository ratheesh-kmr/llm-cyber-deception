import React from 'react';
import { Settings as SettingsIcon, ShieldCheck, Cpu, Database, Server } from 'lucide-react';

export default function Settings() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div>
        <h1 style={{ fontSize: '24px', fontWeight: '700', color: '#f8fafc' }}>System Configuration</h1>
        <p style={{ color: '#94a3b8', fontSize: '14px', marginTop: '4px' }}>
          Deception engine parameters, safety boundaries, and active LLM integration settings.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '20px' }}>
        <div className="glass-card" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', color: '#38bdf8', marginBottom: '16px' }}>
            <Cpu style={{ width: '20px', height: '20px' }} />
            <h3 style={{ fontSize: '16px', color: '#f8fafc' }}>LLM Provider Engine</h3>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', fontSize: '13px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 0', borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
              <span style={{ color: '#94a3b8' }}>Active Provider:</span>
              <span style={{ color: '#10b981', fontWeight: '600' }}>Mock Provider (Demo Mode)</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 0', borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
              <span style={{ color: '#94a3b8' }}>Ollama Local Model:</span>
              <span style={{ color: '#f8fafc' }}>http://localhost:11434 (llama3)</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 0' }}>
              <span style={{ color: '#94a3b8' }}>Fallback to Mock:</span>
              <span style={{ color: '#10b981' }}>Enabled</span>
            </div>
          </div>
        </div>

        <div className="glass-card" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', color: '#a855f7', marginBottom: '16px' }}>
            <ShieldCheck style={{ width: '20px', height: '20px' }} />
            <h3 style={{ fontSize: '16px', color: '#f8fafc' }}>Security & Safety Guardrails</h3>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', fontSize: '13px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 0', borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
              <span style={{ color: '#94a3b8' }}>Synthetic Marker Enforced:</span>
              <span style={{ color: '#10b981', fontWeight: '600' }}>ACTIVE (True)</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 0', borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
              <span style={{ color: '#94a3b8' }}>Prohibited Commands Filter:</span>
              <span style={{ color: '#10b981' }}>Enforced (LureValidator)</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 0' }}>
              <span style={{ color: '#94a3b8' }}>Lure Generation Risk Threshold:</span>
              <span className="mono" style={{ color: '#f8fafc', fontWeight: '700' }}>Score &ge; 4.0</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
