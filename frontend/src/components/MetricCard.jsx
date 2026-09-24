import React from 'react';

export default function MetricCard({ title, value, subtext, icon: Icon, color = '#38bdf8' }) {
  return (
    <div className="glass-card" style={{ padding: '20px 24px', position: 'relative', overflow: 'hidden' }}>
      <div style={{ display: 'flex', justifySelf: 'space-between', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <span style={{ fontSize: '13px', color: '#94a3b8', fontWeight: '500', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
            {title}
          </span>
          <div className="mono" style={{ fontSize: '28px', fontWeight: '700', color: '#f8fafc', marginTop: '6px' }}>
            {value}
          </div>
          {subtext && (
            <div style={{ fontSize: '12px', color: '#64748b', marginTop: '4px' }}>
              {subtext}
            </div>
          )}
        </div>
        <div style={{
          width: '44px',
          height: '44px',
          borderRadius: '10px',
          background: `${color}15`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          border: `1px solid ${color}30`
        }}>
          {Icon && <Icon style={{ width: '22px', height: '22px', color }} />}
        </div>
      </div>
    </div>
  );
}
