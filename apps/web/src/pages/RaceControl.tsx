import { useEffect, useState, useCallback } from 'react'

interface Lane { lane_id: string; lane_name: string; workstream: string; completion_pct: number; blocked_count: number; on_track: boolean; status: string }
interface Incident { incident_id: string; incident_title: string; severity: string; status: string; reported_at: string }
interface Score { score_id: string; overall_health: string; sla_adherence_pct: number; blocker_count: number; checkpoints_passed: number; checkpoints_total: number }
interface Checkpoint { checkpoint_id: string; checkpoint_name: string; criteria_met: boolean; gate_result: string; status: string }
interface Approval { approval_id: string; approval_level: number; total_levels: number; all_approved: boolean; status: string }
interface SecurityEvent { event_id: string; event_type: string; severity: string; path_attempted: string; status: string; blocked: boolean; fix_applied: boolean }

export default function RaceControl() {
  const [lanes, setLanes] = useState<Lane[]>([])
  const [incidents, setIncidents] = useState<Incident[]>([])
  const [scores, setScores] = useState<Score[]>([])
  const [checkpoints, setCheckpoints] = useState<Checkpoint[]>([])
  const [approvals, setApprovals] = useState<Approval[]>([])
  const [securityEvents, setSecurityEvents] = useState<SecurityEvent[]>([])
  const [stateInfo, setStateInfo] = useState<string>('Loading...')

  // Run Golden state
  const [runStatus, setRunStatus] = useState<string>('')
  const [runLoading, setRunLoading] = useState(false)

  // Export badges
  const [telemBadge, setTelemBadge] = useState<string>('')
  const [courtBadge, setCourtBadge] = useState<string>('')

  // Replay section
  const [replayOpen, setReplayOpen] = useState(false)
  const [replayHash, setReplayHash] = useState<string>('')
  const [replayLoading, setReplayLoading] = useState(false)

  // Dossier modal
  const [dossierTitle, setDossierTitle] = useState<string>('')
  const [dossierContent, setDossierContent] = useState<string>('')
  const [dossierOpen, setDossierOpen] = useState(false)

  const loadAll = useCallback(() => {
    Promise.all([
      fetch('/api/lane-status').then(r => r.json()),
      fetch('/api/incident-log').then(r => r.json()),
      fetch('/api/live-scoreboard').then(r => r.json()),
      fetch('/api/close-checkpoint').then(r => r.json()),
      fetch('/api/rc-approval').then(r => r.json()),
      fetch('/api/rc-state-machine').then(r => r.json()),
      fetch('/api/ops/security-events').then(r => r.json()).catch(() => ({ items: [] })),
    ]).then(([ln, inc, sc, cp, ap, sm, sec]) => {
      setLanes(ln.items || [])
      setIncidents(inc.items || [])
      setScores(sc.items || [])
      setCheckpoints(cp.items || [])
      setApprovals(ap.items || [])
      setSecurityEvents(sec.items || [])
      const machineCount = sm.items?.length || 0
      setStateInfo(`${machineCount} state machine(s) active`)
    }).catch(() => setStateInfo('Error loading RC data'))
  }, [])

  useEffect(() => { loadAll() }, [loadAll])

  const healthColor = (h: string) => {
    if (h === 'green') return 'bg-green-100 text-green-800'
    if (h === 'yellow') return 'bg-yellow-100 text-yellow-800'
    return 'bg-red-100 text-red-800'
  }

  const severityColor = (s: string) => {
    if (s === 'critical') return 'bg-red-600 text-white'
    if (s === 'high') return 'bg-orange-500 text-white'
    if (s === 'medium') return 'bg-yellow-400 text-gray-900'
    return 'bg-gray-200 text-gray-700'
  }

  // --- Actions ---
  const runGolden = async () => {
    setRunLoading(true)
    setRunStatus('')
    try {
      const r = await fetch('/api/ops/golden-scenario-run', { method: 'POST' })
      const j = await r.json()
      setRunStatus(j.status === 'seeded' ? 'SEEDED' : j.status || 'OK')
      loadAll()
    } catch {
      setRunStatus('ERROR')
    } finally {
      setRunLoading(false)
    }
  }

  const openDossier = async (title: string, url: string) => {
    setDossierTitle(title)
    setDossierContent('Loading...')
    setDossierOpen(true)
    try {
      const r = await fetch(url)
      const j = await r.json()
      setDossierContent(JSON.stringify(j, null, 2))
    } catch {
      setDossierContent('Failed to load dossier')
    }
  }

  const approveStep = async (approvalId: string) => {
    await fetch(`/api/ops/rc-approval/${approvalId}/approve`, { method: 'POST' })
    loadAll()
  }

  const exportTelemetry = async () => {
    const r = await fetch('/api/ops/export/telemetry-pack', { method: 'POST' })
    const j = await r.json()
    setTelemBadge(j.status || 'PASS')
  }

  const exportCourt = async () => {
    const r = await fetch('/api/ops/export/court-pack', { method: 'POST' })
    const j = await r.json()
    setCourtBadge(j.status || 'PASS')
  }

  const regenBinder = async () => {
    setReplayLoading(true)
    const r = await fetch('/api/ops/replay/regenerate-binder', { method: 'POST' })
    const j = await r.json()
    setReplayHash(j.binder_hash || j.hash || '')
    setReplayLoading(false)
  }

  const fixSecurityPath = async (eventId: string) => {
    await fetch(`/api/ops/security-event/${eventId}/fix-path`, { method: 'POST' })
    loadAll()
  }

  return (
    <div data-testid="race-control-page" className="pb-10">
      <div className="flex flex-wrap items-center justify-between gap-3 mb-1">
        <div className="flex items-center gap-3">
          <h1 className="text-2xl font-bold" data-testid="rc-title">Race Control</h1>
          <span
            data-testid="f1-theme-badge"
            className="px-3 py-1 bg-yellow-500 text-black rounded-full text-xs font-bold flex-shrink-0"
          >
            🏁 Race Beyond the Track
          </span>
        </div>
        <div className="flex items-center gap-2">
          <button
            data-testid="race-control-run-golden"
            onClick={runGolden}
            disabled={runLoading}
            className="px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-semibold hover:bg-indigo-700 disabled:opacity-50 transition"
          >
            {runLoading ? 'Seedingâ€¦' : 'â–· Run Canonical'}
          </button>
          {runStatus && (
            <span
              data-testid="rc-run-status"
              className={`px-3 py-1 rounded-full text-xs font-bold ${runStatus === 'SEEDED' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}
            >
              {runStatus}
            </span>
          )}
        </div>
      </div>

      <p className="text-gray-500 mb-6" data-testid="rc-subtitle">
        Close orchestration command center â€” monitor lanes, SLAs, incidents, checkpoints, and approvals.
      </p>

      {/* State Machine Info */}
      <div className="mb-6 flex gap-3 flex-wrap" data-testid="rc-state-info">
        <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800">
          ðŸ {stateInfo}
        </span>
      </div>

      {/* Scoreboard Summary */}
      {scores.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6" data-testid="rc-scoreboard">
          {scores.slice(0, 3).map(s => (
            <div key={s.score_id} className={`p-4 rounded-lg shadow ${healthColor(s.overall_health)}`} data-testid="rc-score-card">
              <div className="text-lg font-semibold">Health: {s.overall_health}</div>
              <div className="text-sm mt-1">SLA: {s.sla_adherence_pct}% | Blockers: {s.blocker_count}</div>
              <div className="text-sm">Checkpoints: {s.checkpoints_passed}/{s.checkpoints_total}</div>
            </div>
          ))}
        </div>
      )}

      {/* Lane Status Board */}
      <section className="mb-6" data-testid="rc-lanes-section">
        <h2 className="text-lg font-semibold mb-3">Lane Status Board</h2>
        {lanes.length === 0 ? (
          <p className="text-gray-400 text-sm">No lanes configured. Click "Run Canonical" to seed.</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {lanes.map(l => (
              <div key={l.lane_id} className="border rounded-lg p-3 shadow-sm" data-testid="rc-lane-card">
                <div className="flex justify-between items-center mb-2">
                  <span className="font-medium">{l.lane_name}</span>
                  <span className={`px-2 py-0.5 rounded text-xs font-medium ${l.on_track ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                    {l.on_track ? 'On Track' : 'At Risk'}
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2 mb-1">
                  <div className="bg-blue-600 h-2 rounded-full" style={{ width: `${Math.min(l.completion_pct, 100)}%` }} />
                </div>
                <div className="flex justify-between text-xs text-gray-500">
                  <span>{l.completion_pct}% complete</span>
                  <span>{l.blocked_count} blocked</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>

      {/* Checkpoints */}
      <section className="mb-6" data-testid="rc-checkpoints-section">
        <h2 className="text-lg font-semibold mb-3">Close Checkpoints</h2>
        {checkpoints.length === 0 ? (
          <p className="text-gray-400 text-sm">No checkpoints defined.</p>
        ) : (
          <table className="w-full text-sm border-collapse" data-testid="rc-checkpoints-table">
            <thead>
              <tr className="bg-gray-50 text-left">
                <th className="px-3 py-2 border">Checkpoint</th>
                <th className="px-3 py-2 border">Criteria Met</th>
                <th className="px-3 py-2 border">Gate Result</th>
                <th className="px-3 py-2 border">Status</th>
                <th className="px-3 py-2 border">Actions</th>
              </tr>
            </thead>
            <tbody>
              {checkpoints.map((cp, idx) => (
                <tr key={cp.checkpoint_id} className="hover:bg-gray-50" data-testid="rc-checkpoint-row">
                  <td className="px-3 py-2 border font-medium">{cp.checkpoint_name}</td>
                  <td className="px-3 py-2 border">{cp.criteria_met ? 'âœ…' : 'âŒ'}</td>
                  <td className="px-3 py-2 border">{cp.gate_result}</td>
                  <td className="px-3 py-2 border">{cp.status}</td>
                  <td className="px-3 py-2 border">
                    <div className="flex gap-1">
                      <button
                        data-testid={`rc-checkpoint-why-${idx}`}
                        onClick={() => openDossier(`Why: ${cp.checkpoint_name}`, `/api/ops/checkpoint/${cp.checkpoint_id}/why`)}
                        className="px-2 py-0.5 text-xs bg-blue-100 text-blue-700 rounded hover:bg-blue-200"
                      >Why</button>
                      <button
                        data-testid={`rc-checkpoint-verify-${idx}`}
                        onClick={() => openDossier(`Verify: ${cp.checkpoint_name}`, `/api/ops/checkpoint/${cp.checkpoint_id}/verify`)}
                        className="px-2 py-0.5 text-xs bg-purple-100 text-purple-700 rounded hover:bg-purple-200"
                      >Verify</button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>

      {/* Incidents */}
      <section className="mb-6" data-testid="rc-incidents-section">
        <h2 className="text-lg font-semibold mb-3">Incident Log</h2>
        {incidents.length === 0 ? (
          <p className="text-gray-400 text-sm">No incidents recorded.</p>
        ) : (
          <div className="space-y-2">
            {incidents.map((inc, idx) => (
              <div key={inc.incident_id} className="border rounded p-3 flex justify-between items-center" data-testid="rc-incident-card">
                <div>
                  <span className="font-medium">{inc.incident_title}</span>
                  <span className={`ml-2 px-2 py-0.5 rounded text-xs ${severityColor(inc.severity)}`}>{inc.severity}</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-xs text-gray-500">{inc.status}</span>
                  <button
                    data-testid={`rc-incident-why-${idx}`}
                    onClick={() => openDossier(`Why: ${inc.incident_title}`, `/api/ops/incident/${inc.incident_id}/why`)}
                    className="px-2 py-0.5 text-xs bg-blue-100 text-blue-700 rounded hover:bg-blue-200"
                  >Why</button>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>

      {/* Approvals */}
      <section className="mb-6" data-testid="rc-approvals-section">
        <h2 className="text-lg font-semibold mb-3">Approval Chain</h2>
        {approvals.length === 0 ? (
          <p className="text-gray-400 text-sm">No approval chains active.</p>
        ) : (
          <table className="w-full text-sm border-collapse" data-testid="rc-approvals-table">
            <thead>
              <tr className="bg-gray-50 text-left">
                <th className="px-3 py-2 border">Approval</th>
                <th className="px-3 py-2 border">Level</th>
                <th className="px-3 py-2 border">All Approved</th>
                <th className="px-3 py-2 border">Status</th>
                <th className="px-3 py-2 border">Actions</th>
              </tr>
            </thead>
            <tbody>
              {approvals.map((ap, idx) => (
                <tr key={ap.approval_id} className="hover:bg-gray-50" data-testid="rc-approval-row">
                  <td className="px-3 py-2 border font-mono text-xs">{ap.approval_id.slice(0, 8)}</td>
                  <td className="px-3 py-2 border">{ap.approval_level}/{ap.total_levels}</td>
                  <td className="px-3 py-2 border">{ap.all_approved ? 'âœ…' : 'â³'}</td>
                  <td className="px-3 py-2 border">{ap.status}</td>
                  <td className="px-3 py-2 border">
                    <div className="flex gap-1 flex-wrap">
                      {ap.status === 'pending' && (
                        <button
                          data-testid={`rc-approval-approve-${idx}`}
                          onClick={() => approveStep(ap.approval_id)}
                          className="px-2 py-0.5 text-xs bg-green-100 text-green-700 rounded hover:bg-green-200"
                        >Approve</button>
                      )}
                      <button
                        data-testid={`rc-approval-why-${idx}`}
                        onClick={() => openDossier(`Why Approval ${idx + 1}`, `/api/ops/approval/${ap.approval_id}/why`)}
                        className="px-2 py-0.5 text-xs bg-blue-100 text-blue-700 rounded hover:bg-blue-200"
                      >Why</button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>

      {/* Security Events */}
      {securityEvents.length > 0 && (
        <section className="mb-6" data-testid="rc-security-events-section">
          <h2 className="text-lg font-semibold mb-3">Security Events</h2>
          <div className="space-y-2">
            {securityEvents.map((ev, idx) => (
              <div key={ev.event_id} className="border border-red-200 rounded p-3 flex justify-between items-center bg-red-50" data-testid="rc-security-event-card">
                <div>
                  <span className="font-medium text-red-800">{ev.event_type}</span>
                  <span className={`ml-2 px-2 py-0.5 rounded text-xs ${severityColor(ev.severity)}`}>{ev.severity}</span>
                  <div className="text-xs text-gray-500 mt-0.5">Path: {ev.path_attempted}</div>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-xs px-2 py-0.5 rounded bg-red-100 text-red-700">{ev.blocked ? 'BLOCKED' : ev.status}</span>
                  {!ev.fix_applied && (
                    <button
                      data-testid={`rc-security-fix-${idx}`}
                      onClick={() => fixSecurityPath(ev.event_id)}
                      className="px-2 py-0.5 text-xs bg-orange-100 text-orange-700 rounded hover:bg-orange-200"
                    >Fix Path</button>
                  )}
                  {ev.fix_applied && (
                    <span className="px-2 py-0.5 text-xs bg-green-100 text-green-700 rounded" data-testid={`rc-security-fixed-badge-${idx}`}>Fixed âœ“</span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Export Pack Buttons */}
      <section className="mb-6" data-testid="rc-export-section">
        <h2 className="text-lg font-semibold mb-3">Export Packs</h2>
        <div className="flex flex-wrap gap-3">
          <div className="flex items-center gap-2">
            <button
              data-testid="rc-export-telemetry"
              onClick={exportTelemetry}
              className="px-3 py-1.5 bg-teal-600 text-white rounded text-sm font-medium hover:bg-teal-700 transition"
            >Export Telemetry Pack</button>
            {telemBadge && (
              <span
                data-testid="rc-export-telemetry-badge"
                className="px-2 py-0.5 text-xs rounded-full bg-teal-100 text-teal-800 font-bold"
              >{telemBadge}</span>
            )}
          </div>
          <div className="flex items-center gap-2">
            <button
              data-testid="rc-export-court"
              onClick={exportCourt}
              className="px-3 py-1.5 bg-amber-600 text-white rounded text-sm font-medium hover:bg-amber-700 transition"
            >Export Court Pack</button>
            {courtBadge && (
              <span
                data-testid="rc-export-court-badge"
                className="px-2 py-0.5 text-xs rounded-full bg-amber-100 text-amber-800 font-bold"
              >{courtBadge}</span>
            )}
          </div>
        </div>
      </section>

      {/* Replay Viewer */}
      <section className="mb-6" data-testid="rc-replay-section">
        <h2 className="text-lg font-semibold mb-3">Replay Viewer</h2>
        <div className="flex flex-wrap gap-3 items-center">
          <button
            data-testid="rc-replay-open"
            onClick={() => setReplayOpen(v => !v)}
            className="px-3 py-1.5 bg-slate-600 text-white rounded text-sm font-medium hover:bg-slate-700 transition"
          >{replayOpen ? 'Close Replay' : 'Open Replay'}</button>
          {replayOpen && (
            <>
              <button
                data-testid="rc-replay-regen"
                onClick={regenBinder}
                disabled={replayLoading}
                className="px-3 py-1.5 bg-violet-600 text-white rounded text-sm font-medium hover:bg-violet-700 disabled:opacity-50 transition"
              >{replayLoading ? 'Regeneratingâ€¦' : 'Regenerate Binder'}</button>
              {replayHash && (
                <span
                  data-testid="rc-replay-hash-badge"
                  className="px-3 py-1 text-xs font-mono bg-violet-100 text-violet-800 rounded border border-violet-200 max-w-xs truncate"
                  title={replayHash}
                >{replayHash}</span>
              )}
            </>
          )}
        </div>
      </section>

      {/* Dossier Modal */}
      {dossierOpen && (
        <div
          className="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
          data-testid="rc-dossier-modal"
          onClick={e => { if (e.target === e.currentTarget) setDossierOpen(false) }}
        >
          <div className="bg-white rounded-xl shadow-2xl w-full max-w-lg mx-4 overflow-hidden">
            <div className="flex items-center justify-between px-5 py-3 bg-indigo-600 text-white">
              <h3 className="font-semibold text-sm">{dossierTitle}</h3>
              <button
                data-testid="rc-dossier-close"
                onClick={() => setDossierOpen(false)}
                className="text-white/80 hover:text-white text-lg leading-none"
              >âœ•</button>
            </div>
            <pre className="p-5 text-xs overflow-auto max-h-96 bg-gray-50" data-testid="rc-dossier-content">
              {dossierContent}
            </pre>
          </div>
        </div>
      )}
    </div>
  )
}
