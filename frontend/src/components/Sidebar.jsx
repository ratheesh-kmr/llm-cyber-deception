import React from 'react';
import { 
  ShieldAlert, 
  Activity, 
  Radio, 
  FileCode, 
  Target, 
  PlayCircle, 
  ExternalLink, 
  Settings,
  Shield
} from 'lucide-react';

export default function Sidebar({ activeTab, setActiveTab }) {
  const menuItems = [
    { id: 'dashboard', label: 'SOC Dashboard', icon: ShieldAlert },
    { id: 'sessions', label: 'Attack Sessions', icon: Activity },
    { id: 'events', label: 'Telemetry Events', icon: Radio },
    { id: 'lures', label: 'LLM Lure Vault', icon: FileCode },
    { id: 'interactions', label: 'Lure Interactions', icon: Target },
    { id: 'simulation', label: 'Attack Simulator', icon: PlayCircle },
    { id: 'settings', label: 'System Settings', icon: Settings },
  ];

  return (
    <aside style={{
      width: '260px',
      background: 'rgba(15, 23, 42, 0.95)',
      borderRight: '1px solid var(--border-color)',
      display: 'flex',
      flexDirection: 'column',
      padding: '24px 16px',
      height: '100vh',
      position: 'sticky',
      top: 0
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '36px', paddingLeft: '8px' }}>
        <div style={{
          width: '38px',
          height: '38px',
          borderRadius: '10px',
          background: 'linear-gradient(135deg, #0284c7, #38bdf8)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: '0 0 16px rgba(56, 189, 248, 0.4)'
        }}>
          <Shield style={{ color: 'white', width: '22px', height: '22px' }} />
        </div>
        <div>
          <h2 style={{ fontSize: '16px', fontWeight: '700', color: '#f8fafc', lineHeight: 1.2 }}>CYBER DECEPTION</h2>
          <span style={{ fontSize: '11px', color: '#38bdf8', fontWeight: '600', letterSpacing: '1px' }}>ACTIVE SOC v1.0</span>
        </div>
      </div>

      <nav style={{ display: 'flex', flexDirection: 'column', gap: '6px', flex: 1 }}>
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                padding: '12px 16px',
                borderRadius: '8px',
                border: 'none',
                background: isActive ? 'rgba(56, 189, 248, 0.12)' : 'transparent',
                color: isActive ? '#38bdf8' : '#94a3b8',
                fontWeight: isActive ? '600' : '400',
                fontSize: '14px',
                cursor: 'pointer',
                textAlign: 'left',
                transition: 'all 0.15s ease'
              }}
            >
              <Icon style={{ width: '18px', height: '18px', color: isActive ? '#38bdf8' : '#64748b' }} />
              {item.label}
            </button>
          );
        })}
      </nav>

      <div style={{
        marginTop: 'auto',
        padding: '16px',
        borderRadius: '8px',
        background: 'rgba(30, 41, 59, 0.5)',
        border: '1px solid var(--border-color)'
      }}>
        <div style={{ fontSize: '12px', color: '#94a3b8', marginBottom: '8px' }}>Target Deception Portal</div>
        <a 
          href="http://127.0.0.1:8001" 
          target="_blank" 
          rel="noreferrer"
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '6px',
            fontSize: '13px',
            color: '#38bdf8',
            textDecoration: 'none',
            fontWeight: '600'
          }}
        >
          Open Fake Portal <ExternalLink style={{ width: '14px', height: '14px' }} />
        </a>
      </div>
    </aside>
  );
}
