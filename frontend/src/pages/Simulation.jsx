import React, { useState, useEffect, useRef } from 'react';
import { 
  Play, 
  Square, 
  Terminal as TerminalIcon, 
  ShieldAlert, 
  Radio, 
  Sparkles, 
  CheckCircle2, 
  AlertTriangle, 
  RotateCcw, 
  Cpu, 
  Zap, 
  Crosshair,
  ArrowRight,
  Flame,
  Globe
} from 'lucide-react';
import { getSimulationScenarios } from '../services/api';

const STAGES = [
  'RECONNAISSANCE',
  'RESOURCE_DISCOVERY',
  'CONFIGURATION_DISCOVERY',
  'CREDENTIAL_DISCOVERY',
  'LURE_INTERACTION',
  'CREDENTIAL_ATTEMPT'
];

export default function Simulation({ onRefresh }) {
  const [scenarios, setScenarios] = useState([]);
  const [selectedScenarioId, setSelectedScenarioId] = useState('basic_recon');
  const [speed, setSpeed] = useState(0.5); // 0.5s multiplier default
  const [isRunning, setIsRunning] = useState(false);
  const [logs, setLogs] = useState([]);
  const [currentStep, setCurrentStep] = useState(null);
  const [riskScore, setRiskScore] = useState(0.0);
  const [activeStage, setActiveStage] = useState('RECONNAISSANCE');
  const [behaviorType, setBehaviorType] = useState('RECONNAISSANCE');
  const [deployedLures, setDeployedLures] = useState([]);
  const [entrapmentAlert, setEntrapmentAlert] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const [summaryStatus, setSummaryStatus] = useState(null);

  const eventSourceRef = useRef(null);
  const terminalBottomRef = useRef(null);

  useEffect(() => {
    getSimulationScenarios()
      .then(data => {
        setScenarios(data);
        if (data.length > 0) setSelectedScenarioId(data[0].scenario_id);
      })
      .catch(console.error);
  }, []);

  // Auto-scroll terminal to bottom on new log
  useEffect(() => {
    if (terminalBottomRef.current) {
      terminalBottomRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [logs]);

  const startLiveSimulation = (scenarioIdToRun = selectedScenarioId) => {
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
    }

    setIsRunning(true);
    setLogs([]);
    setCurrentStep(null);
    setRiskScore(0.0);
    setActiveStage('RECONNAISSANCE');
    setBehaviorType('RECONNAISSANCE');
    setDeployedLures([]);
    setEntrapmentAlert(null);
    setSummaryStatus(null);

    const sseUrl = `/api/simulation/stream?scenario_id=${scenarioIdToRun}&speed=${speed}`;
    const es = new EventSource(sseUrl);
    eventSourceRef.current = es;

    addLog('system', `[SYS] Connecting to Deception Gateway telemetry stream...`);

    es.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        handleStreamEvent(data);
      } catch (err) {
        console.error('Error parsing SSE event', err);
      }
    };

    es.onerror = (err) => {
      console.warn('Simulation stream finished or closed', err);
      es.close();
      setIsRunning(false);
      if (onRefresh) onRefresh();
    };
  };

  const handleStreamEvent = (data) => {
    switch (data.type) {
      case 'scenario_start':
        setSessionId(data.session_id);
        addLog('info', `[SESSION INITIALIZED] Target Host: ${data.target_host} | Session: ${data.session_id.substring(0, 8)}...`);
        addLog('red', `[RED TEAM] Launching campaign: ${data.scenario_name} (${data.total_steps} sequential vectors)`);
        break;

      case 'step_start':
        setCurrentStep(data);
        addLog('red', `[PROBE #${data.step_index}/${data.total_steps}] ${data.method} ${data.path} -- ${data.description}`);
        break;

      case 'lure_deployed':
        setDeployedLures(prev => [...prev, data]);
        addLog('ai', `🤖 [AI DECEPTION ENGINE] Threshold crossed! Synthesized honey-lure "${data.title}" -> Deployed at ${data.endpoint_path}`);
        break;

      case 'step_finish':
        setRiskScore(data.risk_score);
        setActiveStage(data.attack_stage);
        setBehaviorType(data.behavior_type);
        const statusColor = data.status_code === 200 ? 'text-emerald' : data.status_code === 401 ? 'text-amber' : 'text-slate';
        addLog('blue', `[GATEWAY] ${data.method} ${data.path} => HTTP ${data.status_code} (${data.duration_ms}ms) | Risk Score: ${data.risk_score} [${data.attack_stage}]`);
        break;

      case 'entrapment_probe':
        addLog('amber', `[RED TEAM RECON] Attacker discovered newly advertised asset: ${data.lure_url}`);
        break;

      case 'lure_entrapped':
        setRiskScore(data.final_risk_score);
        setActiveStage(data.attack_stage);
        setEntrapmentAlert(data);
        addLog('critical', `⚡ [HONEY-TOKEN TRAP TRIGGERED] Attacker downloaded fake credential artifact! Risk boosted to ${data.final_risk_score}. Attribution confirmed.`);
        break;

      case 'scenario_complete':
        setIsRunning(false);
        setSummaryStatus(data);
        addLog('success', `✔ [CAMPAIGN TERMINATED] All ${data.steps_completed} vectors executed. Final Threat Score: ${data.final_risk_score}`);
        if (eventSourceRef.current) eventSourceRef.current.close();
        if (onRefresh) onRefresh();
        break;

      case 'error':
        addLog('critical', `[ERROR] ${data.message}`);
        setIsRunning(false);
        if (eventSourceRef.current) eventSourceRef.current.close();
        break;

      default:
        break;
    }
  };

  const stopSimulation = () => {
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
    }
    setIsRunning(false);
    addLog('system', `[SYS] Simulation manually aborted by SOC analyst.`);
  };

  const addLog = (level, text) => {
    const time = new Date().toLocaleTimeString();
    setLogs(prev => [...prev, { time, level, text }]);
  };

  const selectedScenario = scenarios.find(s => s.scenario_id === selectedScenarioId);

  // Compute Risk Level Color
  const getRiskColor = (score) => {
    if (score >= 11) return '#ef4444';
    if (score >= 7) return '#f97316';
    if (score >= 3) return '#f59e0b';
    return '#10b981';
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* War Room Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{
              width: '10px',
              height: '10px',
              borderRadius: '50%',
              background: isRunning ? '#ef4444' : '#10b981'
            }} className={isRunning ? 'pulse-dot' : 'pulse-green'} />
            <span style={{ fontSize: '12px', fontWeight: '700', color: isRunning ? '#ef4444' : '#10b981', letterSpacing: '1px' }}>
              {isRunning ? 'LIVE ATTACK ENGAGEMENT IN PROGRESS' : 'WAR ROOM STANDBY'}
            </span>
          </div>
          <h1 style={{ fontSize: '24px', fontWeight: '700', color: '#f8fafc', marginTop: '4px' }}>
            Cyber Attack Live Simulation Studio
          </h1>
          <p style={{ color: '#94a3b8', fontSize: '13px', marginTop: '2px' }}>
            Watch realistic adversary attack campaigns execute live against the deception gateway while the autonomous AI traps them.
          </p>
        </div>

        {/* Controls */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          {/* Scenario Dropdown */}
          <select
            disabled={isRunning}
            value={selectedScenarioId}
            onChange={(e) => setSelectedScenarioId(e.target.value)}
            style={{
              padding: '10px 14px',
              borderRadius: '8px',
              background: 'rgba(30, 41, 59, 0.8)',
              border: '1px solid var(--border-color)',
              color: '#f8fafc',
              fontSize: '13px',
              fontWeight: '600',
              outline: 'none',
              cursor: isRunning ? 'not-allowed' : 'pointer'
            }}
          >
            {scenarios.map(s => (
              <option key={s.scenario_id} value={s.scenario_id}>
                {s.name} ({s.step_count} steps)
              </option>
            ))}
          </select>

          {/* Speed Selector */}
          <div style={{ display: 'flex', background: 'rgba(30, 41, 59, 0.6)', padding: '4px', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
            {[
              { val: 0.8, label: '1x Cinematic' },
              { val: 0.4, label: '2x Fast' },
              { val: 0.15, label: '5x Turbo' }
            ].map(sp => (
              <button
                key={sp.val}
                disabled={isRunning}
                onClick={() => setSpeed(sp.val)}
                style={{
                  padding: '6px 12px',
                  borderRadius: '6px',
                  border: 'none',
                  background: speed === sp.val ? 'rgba(56, 189, 248, 0.2)' : 'transparent',
                  color: speed === sp.val ? '#38bdf8' : '#94a3b8',
                  fontSize: '12px',
                  fontWeight: '600',
                  cursor: isRunning ? 'not-allowed' : 'pointer'
                }}
              >
                {sp.label}
              </button>
            ))}
          </div>

          {/* Action Buttons */}
          {isRunning ? (
            <button
              onClick={stopSimulation}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                padding: '10px 20px',
                borderRadius: '8px',
                background: '#ef4444',
                color: 'white',
                border: 'none',
                fontWeight: '700',
                fontSize: '13px',
                cursor: 'pointer',
                boxShadow: '0 0 20px rgba(239, 68, 68, 0.4)'
              }}
            >
              <Square style={{ width: '15px', height: '15px' }} /> Abort Attack
            </button>
          ) : (
            <button
              onClick={() => startLiveSimulation()}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                padding: '10px 22px',
                borderRadius: '8px',
                background: 'linear-gradient(135deg, #0284c7, #38bdf8)',
                color: 'white',
                border: 'none',
                fontWeight: '700',
                fontSize: '13px',
                cursor: 'pointer',
                boxShadow: '0 0 20px rgba(56, 189, 248, 0.35)'
              }}
            >
              <Play style={{ width: '15px', height: '15px' }} /> Launch Live Attack
            </button>
          )}
        </div>
      </div>

      {/* DUAL-CONSOLE WAR ROOM INTERFACE */}
      <div style={{ display: 'grid', gridTemplateColumns: '1.15fr 0.85fr', gap: '20px' }}>
        
        {/* LEFT PANE: 🔴 RED TEAM ATTACKER TERMINAL */}
        <div className="terminal-window">
          <div className="terminal-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <div className="terminal-dot" style={{ background: '#ef4444' }} />
              <div className="terminal-dot" style={{ background: '#f59e0b' }} />
              <div className="terminal-dot" style={{ background: '#10b981' }} />
              <span className="mono" style={{ fontSize: '12px', color: '#94a3b8', marginLeft: '8px' }}>
                attacker@kali-recon: ~/{selectedScenarioId}
              </span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span className="mono" style={{ fontSize: '11px', color: '#64748b' }}>IP: 192.168.1.100</span>
              <button
                onClick={() => setLogs([])}
                style={{ background: 'none', border: 'none', color: '#64748b', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '4px', fontSize: '11px' }}
                title="Clear Logs"
              >
                <RotateCcw style={{ width: '12px', height: '12px' }} /> Clear
              </button>
            </div>
          </div>

          <div className="terminal-body" style={{ minHeight: '440px' }}>
            {logs.length === 0 ? (
              <div style={{ color: '#475569', textAlign: 'center', paddingTop: '140px' }}>
                <TerminalIcon style={{ width: '36px', height: '36px', margin: '0 auto 10px', opacity: 0.3 }} />
                <div>Attack console ready. Select a scenario above and click "Launch Live Attack" to initiate.</div>
              </div>
            ) : (
              logs.map((log, index) => {
                let color = '#94a3b8';
                if (log.level === 'red') color = '#f87171';
                else if (log.level === 'blue') color = '#38bdf8';
                else if (log.level === 'ai') color = '#c084fc';
                else if (log.level === 'amber') color = '#fcd34d';
                else if (log.level === 'critical') color = '#ef4444';
                else if (log.level === 'success') color = '#4ade80';

                return (
                  <div key={index} style={{ marginBottom: '6px', color, wordBreak: 'break-all' }}>
                    <span style={{ color: '#475569', marginRight: '8px', fontSize: '11px' }}>[{log.time}]</span>
                    {log.text}
                  </div>
                );
              })
            )}
            <div ref={terminalBottomRef} />
          </div>

          {/* Terminal Footer Status Bar */}
          <div style={{
            background: '#090d16',
            padding: '8px 16px',
            borderTop: '1px solid rgba(255, 255, 255, 0.06)',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            fontSize: '11px',
            color: '#64748b'
          }}>
            <span className="mono">Target Gateway: http://127.0.0.1:8000/gateway</span>
            <span className="mono">Status: {isRunning ? 'PROBING ACTIVELY' : 'IDLE'}</span>
          </div>
        </div>

        {/* RIGHT PANE: 🔵 BLUE TEAM DEFENSE & DECEPTION COCKPIT */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          
          {/* Dynamic Risk Meter & Stage Header */}
          <div className="glass-card" style={{ padding: '20px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
              <div>
                <span style={{ fontSize: '11px', color: '#94a3b8', fontWeight: '700' }}>ADVERSARY THREAT SCORE</span>
                <div style={{ display: 'flex', alignItems: 'baseline', gap: '8px', marginTop: '2px' }}>
                  <span className="mono" style={{ fontSize: '32px', fontWeight: '800', color: getRiskColor(riskScore) }}>
                    {riskScore.toFixed(1)}
                  </span>
                  <span style={{
                    fontSize: '12px',
                    fontWeight: '700',
                    color: getRiskColor(riskScore),
                    textTransform: 'uppercase'
                  }}>
                    {riskScore >= 11 ? 'CRITICAL' : riskScore >= 7 ? 'HIGH' : riskScore >= 3 ? 'MEDIUM' : 'LOW'}
                  </span>
                </div>
              </div>

              <div style={{ textAlign: 'right' }}>
                <span style={{ fontSize: '11px', color: '#94a3b8', fontWeight: '700' }}>CLASSIFIED TARGET</span>
                <div className="mono" style={{ fontSize: '15px', color: '#c084fc', fontWeight: '700', marginTop: '4px' }}>
                  {behaviorType}
                </div>
              </div>
            </div>

            {/* Risk Gauge Progress Bar */}
            <div style={{ width: '100%', height: '8px', background: 'rgba(255, 255, 255, 0.08)', borderRadius: '4px', overflow: 'hidden' }}>
              <div style={{
                width: `${Math.min(100, (riskScore / 20) * 100)}%`,
                height: '100%',
                background: `linear-gradient(90deg, #10b981, #f59e0b, #ef4444)`,
                transition: 'width 0.4s ease'
              }} />
            </div>
          </div>

          {/* Attack Stage Progression Stepper */}
          <div className="glass-card" style={{ padding: '20px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px' }}>
              <span style={{ fontSize: '11px', color: '#94a3b8', fontWeight: '700' }}>STAGE PROFILING ENGINE</span>
              <span className="mono" style={{ fontSize: '11px', color: '#38bdf8' }}>STAGE: {activeStage}</span>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
              {STAGES.map((st, idx) => {
                const currentIdx = STAGES.indexOf(activeStage);
                const isCurrent = idx === currentIdx;
                const isPassed = idx < currentIdx;

                return (
                  <div
                    key={st}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '10px',
                      padding: '7px 10px',
                      borderRadius: '6px',
                      background: isCurrent ? 'rgba(56, 189, 248, 0.15)' : isPassed ? 'rgba(16, 185, 129, 0.08)' : 'rgba(255, 255, 255, 0.02)',
                      border: isCurrent ? '1px solid #38bdf8' : '1px solid transparent',
                      transition: 'all 0.3s ease'
                    }}
                  >
                    <div style={{
                      width: '18px',
                      height: '18px',
                      borderRadius: '50%',
                      background: isCurrent ? '#38bdf8' : isPassed ? '#10b981' : '#334155',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      fontSize: '10px',
                      fontWeight: 'bold',
                      color: 'white'
                    }}>
                      {idx + 1}
                    </div>
                    <span style={{
                      fontSize: '11px',
                      fontWeight: isCurrent ? '700' : '500',
                      color: isCurrent ? '#38bdf8' : isPassed ? '#e2e8f0' : '#64748b'
                    }}>
                      {st.replace(/_/g, ' ')}
                    </span>
                    {isCurrent && (
                      <span style={{ marginLeft: 'auto', fontSize: '9px', padding: '2px 6px', borderRadius: '4px', background: '#38bdf8', color: '#090d16', fontWeight: 'bold' }}>
                        ACTIVE
                      </span>
                    )}
                  </div>
                );
              })}
            </div>
          </div>

          {/* Dynamic AI Deception Action Alert */}
          {entrapmentAlert ? (
            <div className="glass-card glow-rose" style={{ padding: '18px', background: 'rgba(239, 68, 68, 0.12)', border: '1px solid #ef4444' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#ef4444', fontWeight: '700', fontSize: '13px' }}>
                <Flame style={{ width: '18px', height: '18px' }} /> ADVERSARY TRAPPED & CONFIRMED
              </div>
              <p style={{ fontSize: '12px', color: '#fca5a5', marginTop: '6px' }}>
                The attacker ingested the synthetic honey-token at <strong className="mono">{entrapmentAlert.endpoint}</strong>. 
                Deception success validated!
              </p>
            </div>
          ) : deployedLures.length > 0 ? (
            <div className="glass-card glow-cyan" style={{ padding: '18px', background: 'rgba(56, 189, 248, 0.1)', border: '1px solid #38bdf8' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#38bdf8', fontWeight: '700', fontSize: '13px' }}>
                <Sparkles style={{ width: '18px', height: '18px' }} /> SYNTHETIC LURE DEPLOYED
              </div>
              <p style={{ fontSize: '12px', color: '#e2e8f0', marginTop: '6px' }}>
                Autonomous LLM synthesized: <strong className="mono">{deployedLures[deployedLures.length - 1].title}</strong>
              </p>
              <div className="mono" style={{ fontSize: '11px', color: '#94a3b8', marginTop: '4px' }}>
                Active at: {deployedLures[deployedLures.length - 1].endpoint_path}
              </div>
            </div>
          ) : (
            <div className="glass-card" style={{ padding: '18px', textAlign: 'center', color: '#64748b', fontSize: '12px' }}>
              <Cpu style={{ width: '22px', height: '22px', margin: '0 auto 6px', opacity: 0.4 }} />
              Autonomous LLM lure engine armed. Awaiting risk score threshold trigger (&ge; 4.0).
            </div>
          )}

        </div>
      </div>

      {/* Attack Scenarios Quick-Launch Grid */}
      <div>
        <h3 style={{ fontSize: '16px', color: '#f8fafc', marginBottom: '14px' }}>Predefined Attack Scenarios</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '16px' }}>
          {scenarios.map(sc => {
            const isCurrentScenario = selectedScenarioId === sc.scenario_id;

            return (
              <div
                key={sc.scenario_id}
                className="glass-card"
                onClick={() => {
                  setSelectedScenarioId(sc.scenario_id);
                  if (!isRunning) startLiveSimulation(sc.scenario_id);
                }}
                style={{
                  padding: '18px',
                  cursor: isRunning ? 'not-allowed' : 'pointer',
                  border: isCurrentScenario ? '1px solid #38bdf8' : '1px solid var(--border-color)',
                  background: isCurrentScenario ? 'rgba(56, 189, 248, 0.08)' : 'var(--bg-card)',
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'space-between',
                  transition: 'all 0.2s'
                }}
              >
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <h4 style={{ fontSize: '15px', color: '#f8fafc' }}>{sc.name}</h4>
                    <span style={{ fontSize: '11px', background: 'rgba(56, 189, 248, 0.15)', color: '#38bdf8', padding: '2px 8px', borderRadius: '4px', fontWeight: '600' }}>
                      {sc.step_count} VECTORS
                    </span>
                  </div>
                  <p style={{ fontSize: '12px', color: '#94a3b8', marginTop: '8px', lineHeight: 1.4 }}>
                    {sc.description}
                  </p>
                </div>

                <div style={{ marginTop: '16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '11px', borderTop: '1px solid rgba(255,255,255,0.06)', paddingTop: '10px' }}>
                  <span style={{ color: '#64748b' }}>Focus: <strong style={{ color: '#e2e8f0' }}>{sc.expected_interest}</strong></span>
                  <span style={{ color: '#38bdf8', fontWeight: '600', display: 'flex', alignItems: 'center', gap: '4px' }}>
                    Launch Stream &rarr;
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
