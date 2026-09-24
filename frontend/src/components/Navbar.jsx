import React, { useState, useEffect } from 'react';
import { RefreshCw, Radio, Bell } from 'lucide-react';

export default function Navbar({ onRefresh }) {
  const [time, setTime] = useState(new Date().toLocaleTimeString());

  useEffect(() => {
    const timer = setInterval(() => setTime(new Date().toLocaleTimeString()), 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <header style={{
      height: '64px',
      borderBottom: '1px solid var(--border-color)',
      padding: '0 32px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      background: 'rgba(15, 23, 42, 0.8)',
      backdropFilter: 'blur(8px)',
      position: 'sticky',
      top: 0,
      zIndex: 10
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          padding: '6px 12px',
          borderRadius: '20px',
          background: 'rgba(16, 185, 129, 0.1)',
          border: '1px solid rgba(16, 185, 129, 0.3)',
          color: '#10b981',
          fontSize: '12px',
          fontWeight: '600'
        }}>
          <Radio style={{ width: '14px', height: '14px', animation: 'pulse 1.5s infinite' }} />
          SOC MONITORING ACTIVE
        </div>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
        <div className="mono" style={{ fontSize: '13px', color: '#94a3b8' }}>
          {time} UTC
        </div>
        <button
          onClick={onRefresh}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            padding: '8px 14px',
            borderRadius: '6px',
            border: '1px solid var(--border-color)',
            background: 'rgba(30, 41, 59, 0.8)',
            color: '#f3f4f6',
            fontSize: '13px',
            fontWeight: '500',
            cursor: 'pointer',
            transition: 'background 0.2s'
          }}
        >
          <RefreshCw style={{ width: '14px', height: '14px' }} />
          Refresh Live Data
        </button>
      </div>
    </header>
  );
}
