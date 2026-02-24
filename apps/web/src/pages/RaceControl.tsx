import { useEffect, useState } from 'react'

interface Lane { lane_id: string; lane_name: string; workstream: string; completion_pct: number; blocked_count: number; on_track: boolean; status: string }
interface Incident { incident_id: string; incident_title: string; severity: string; status: string; reported_at: string }
interface Score { score_id: string; overall_health: string; sla_adherence_pct: number; blocker_count: number; checkpoints_passed: number; checkpoints_total: number }
interface Checkpoint { checkpoint_id: string; checkpoint_name: string; criteria_met: boolean; gate_result: string; status: string }
interface Approval { approval_id: string; approval_level: number; total_levels: number; all_approved: boolean; status: string }

export default function RaceControl() {
  const [lanes, setLanes] = useState<Lane[]>([])
  const [incidents, setIncidents] = useState<Incident[]>([])
  const [scores, setScores] = useState<Score[]>([])
  const [checkpoints, setCheckpoints] = useState<Checkpoint[]>([])
  const [approvals, setApprovals] = useState<Approval[]>([])
  const [stateInfo, setStateInfo] = useState<string>('Loading...')

  useEffect(() => {
    Promise.all([
      fetch('/api/lane-status').then(r => r.json()),
      fetch('/api/incident-log').then(r => r.json()),
      fetch('/api/live-scoreboard').then(r => r.json()),
      fetch('/api/close-checkpoint').then(r => r.json()),
      fetch('/api/rc-approval').then(r => r.json()),
      fetch('/api/rc-state-machine').then(r => r.json()),
    ]).then(([ln, inc, sc, cp, ap, sm]) => {
      setLanes(ln.items || [])
      setIncidents(inc.items || [])
      setScores(sc.items || [])
      setCheckpoints(cp.items || [])
      setApprovals(ap.items || [])
      const machineCount = sm.items?.length || 0
      setStateInfo(`${machineCount} state machine(s) active`)
    }).catch(() => setStateInfo('Error loading RC data'))
  }, [])

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

  return (
    <div data-testid="race-control-page">
      <h1 className="text-2xl font-bold mb-1" data-testid="rc-title">Race Control</h1>
      <p className="text-gray-500 mb-6" data-testid="rc-subtitle">
        Close orchestration command center — monitor lanes, SLAs, incidents, checkpoints, and approvals.
      </p>

      {/* State Machine Info */}
      <div className="mb-6 flex gap-3 flex-wrap" data-testid="rc-state-info">
        <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800">
          🏁 {stateInfo}
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
          <p className="text-gray-400 text-sm">No lanes configured. Create lane data via API.</p>
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
              </tr>
            </thead>
            <tbody>
              {checkpoints.map(cp => (
                <tr key={cp.checkpoint_id} className="hover:bg-gray-50" data-testid="rc-checkpoint-row">
                  <td className="px-3 py-2 border font-medium">{cp.checkpoint_name}</td>
                  <td className="px-3 py-2 border">{cp.criteria_met ? '✅' : '❌'}</td>
                  <td className="px-3 py-2 border">{cp.gate_result}</td>
                  <td className="px-3 py-2 border">{cp.status}</td>
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
            {incidents.map(inc => (
              <div key={inc.incident_id} className="border rounded p-3 flex justify-between items-center" data-testid="rc-incident-card">
                <div>
                  <span className="font-medium">{inc.incident_title}</span>
                  <span className={`ml-2 px-2 py-0.5 rounded text-xs ${severityColor(inc.severity)}`}>{inc.severity}</span>
                </div>
                <span className="text-xs text-gray-500">{inc.status}</span>
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
              </tr>
            </thead>
            <tbody>
              {approvals.map(ap => (
                <tr key={ap.approval_id} className="hover:bg-gray-50" data-testid="rc-approval-row">
                  <td className="px-3 py-2 border font-mono text-xs">{ap.approval_id.slice(0, 8)}</td>
                  <td className="px-3 py-2 border">{ap.approval_level}/{ap.total_levels}</td>
                  <td className="px-3 py-2 border">{ap.all_approved ? '✅' : '⏳'}</td>
                  <td className="px-3 py-2 border">{ap.status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
    </div>
  )
}
