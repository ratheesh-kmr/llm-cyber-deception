import React from 'react';

export default function RiskBadge({ level }) {
  const normalized = (level || 'LOW').toUpperCase();
  const classes = {
    LOW: 'badge-low',
    MEDIUM: 'badge-medium',
    HIGH: 'badge-high',
    CRITICAL: 'badge-critical'
  };

  return (
    <span className={`badge ${classes[normalized] || 'badge-low'}`}>
      ● {normalized}
    </span>
  );
}
