/**
 * LedgerLive Dashboard — F1 Command Center
 * Mission control for the finance close cycle.
 */
import { useEffect, useState, useCallback } from 'react'
import { Link } from 'react-router-dom'
import { API_BASE } from '../services/api'

// ── Types ─────────────────────────────────────────────────────────────────────
interface Health { project: string; status: string; mode: string; llm: string; ts: string }
interface Counts { docs: number; recons: number; exceptions: number; reviews: number; audits: number }
interface AuditEvent {
  trace_id?: string; id?: string; action: string; actor?: string;
  entity_type?: string; ts: string; detail?: Record<string, unknown>
}
interface Exception {
  id?: string; exception_id?: string; description?: string; message?: string;
  severity?: string; status?: string
}
interface CloseStage { name: string; status: 'done' | 'active' | 'pending'; pct: number }

// ── KPI card ───────────────────────────────────────────────────────────────────
function KpiCard({ label, value, sub, trend, accent, icon, to }: {
  label: string; value: string | number; sub?: string
  trend?: 'up' | 'down' | 'flat'; accent: string; icon: string; to: string
}) {
  const trendColor = trend === 'up' ? 'text-green-400' : trend === 'down' ? 'text-red-400' : 'text-gray-400'
  const trendGlyph = trend === 'up' ? '▲' : trend === 'down' ? '▼' : '—'
  return (
    <Link to={to}
      className="block rounded-xl p-4 bg-[#111118] border border-[#2A2A3A] hover:border-[#3A3A4A] hover:bg-[#141420] transition-all group"
    >
      <div className="flex items-start justify-between mb-2.5">
        <span className="text-xl">{icon}</span>
        <span className={`text-xs font-mono ${trendColor}`}>{trendGlyph}</span>
      </div>
      <div className={`text-2xl font-bold font-mono ${accent} tabular-nums mb-1`}>{value}</div>
      <div className="text-[11px] text-gray-400 font-semibold uppercase tracking-wider">{label}</div>
      {sub && <div className="text-[11px] text-gray-300 mt-0.5 truncate">{sub}</div>}
    </Link>
  )
}

// ── Close cycle progress ───────────────────────────────────────────────────────
function CloseProgress({ stages }: { stages: CloseStage[] }) {
  return (
    <div className="space-y-2.5">
      {stages.map((stage, i) => (
        <div key={i} className="flex items-center gap-3 group">
          <div className={`w-1.5 h-1.5 rounded-full flex-shrink-0 ${
            stage.status === 'done'   ? 'bg-green-500' :
            stage.status === 'active' ? 'bg-blue-400 animate-pulse' : 'bg-gray-700'
          }`} />
          <span className={`text-xs w-36 truncate flex-shrink-0 ${
            stage.status === 'done'   ? 'text-gray-400 line-through' :
            stage.status === 'active' ? 'text-blue-300 font-medium' : 'text-gray-300'
          }`}>{stage.name}</span>
          <div className="flex-1 h-1 bg-[#1E1E2E] rounded-full overflow-hidden">
            <div className={`h-full rounded-full transition-all duration-500 ${
              stage.status === 'done'   ? 'bg-green-500' :
              stage.status === 'active' ? 'bg-blue-500' : 'bg-transparent'
            }`} style={{ width: `${stage.pct}%` }} />
          </div>
          <span className="text-[11px] font-mono text-gray-300 w-8 text-right">{stage.pct}%</span>
        </div>
      ))}
    </div>
  )
}

// ── Severity bar ───────────────────────────────────────────────────────────────
function SeverityBar({ counts }: { counts: Record<string, number> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1
  const bars = [
    { key: 'CRITICAL', color: 'bg-red-600',    label: 'Critical' },
    { key: 'HIGH',     color: 'bg-orange-500', label: 'High' },
    { key: 'MEDIUM',   color: 'bg-yellow-500', label: 'Medium' },
    { key: 'LOW',      color: 'bg-blue-500',   label: 'Low' },
  ]
  return (
    <div>
      <div className="flex h-2 rounded-full overflow-hidden gap-px mb-2">
        {bars.map(b => (
          <div key={b.key} className={`${b.color} transition-all duration-500`}
            style={{ width: `${((counts[b.key] || 0) / total) * 100}%` }} />
        ))}
      </div>
      <div className="flex gap-3 flex-wrap">
        {bars.map(b => (
          <span key={b.key} className="flex items-center gap-1 text-[11px] text-gray-400">
            <span className={`w-1.5 h-1.5 rounded-full ${b.color}`} />
            {counts[b.key] || 0} {b.label}
          </span>
        ))}
      </div>
    </div>
  )
}

// ── Activity feed ──────────────────────────────────────────────────────────────
function ActivityFeed({ events }: { events: AuditEvent[] }) {
  if (!events.length) return (
    <div className="flex flex-col items-center justify-center py-8 text-center">
      <span className="text-2xl mb-2">💤</span>
      <p className="text-xs text-gray-300">No recent activity</p>
    </div>
  )
  return (
    <div className="space-y-0.5">
      {events.slice(0, 9).map((e, i) => (
        <div key={e.trace_id || e.id || i}
          className="flex items-start gap-2 py-1.5 border-b border-[#17171F] last:border-0">
          <span className="w-1 h-1 rounded-full bg-gray-700 mt-2 flex-shrink-0" />
          <div className="flex-1 min-w-0">
            <p className="text-xs text-gray-400 truncate">{e.action}</p>
            {e.actor && <p className="text-[11px] text-gray-300">{e.actor}</p>}
          </div>
          <span className="text-[11px] text-gray-200 flex-shrink-0 font-mono tabular-nums">
            {new Date(e.ts).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </span>
        </div>
      ))}
    </div>
  )
}

// ── Skeleton loader ────────────────────────────────────────────────────────────
function SkeletonGrid() {
  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 animate-pulse">
      {Array.from({ length: 6 }).map((_, i) => (
        <div key={i} className="h-28 rounded-xl bg-[#111118] border border-[#2A2A3A]" />
      ))}
    </div>
  )
}

// ── Main Dashboard ─────────────────────────────────────────────────────────────
export default function Dashboard() {
  const [health, setHealth] = useState<Health | null>(null)
  const [counts, setCounts] = useState<Counts>({ docs: 0, recons: 0, exceptions: 0, reviews: 0, audits: 0 })
  const [activity, setActivity] = useState<AuditEvent[]>([])
  const [exceptions, setExceptions] = useState<Exception[]>([])
  const [loading, setLoading] = useState(true)
  const [liveRunning, setLiveRunning] = useState(false)
  const [lastRefresh, setLastRefresh] = useState(new Date())

  const load = useCallback(() => {
    fetch(`${API_BASE}/api/agent/status`)
      .then(r => r.json())
      .then(d => setLiveRunning(d.status === 'running'))
      .catch(() => {})

    fetch(`${API_BASE}/healthz`).then(r => r.json()).then(setHealth).catch(() => {})

    Promise.all([
      fetch(`${API_BASE}/api/documents`).then(r => r.json()),
      fetch(`${API_BASE}/api/reconciliations`).then(r => r.json()),
      fetch(`${API_BASE}/api/exceptions`).then(r => r.json()),
      fetch(`${API_BASE}/api/reviews`).then(r => r.json()),
      fetch(`${API_BASE}/api/audit`).then(r => r.json()),
    ]).then(([d, rc, ex, rv, au]) => {
      setCounts({
        docs:       d.total  ?? d.items?.length  ?? 0,
        recons:     rc.total ?? rc.items?.length ?? 0,
        exceptions: ex.total ?? ex.items?.length ?? 0,
        reviews:    rv.total ?? rv.items?.length ?? 0,
        audits:     au.total ?? au.items?.length ?? 0,
      })
      setActivity((au.events || au.items || []).slice(0, 9))
      setExceptions((ex.items || []).slice(0, 5))
    }).catch(() => {}).finally(() => setLoading(false))

    setLastRefresh(new Date())
  }, [])

  useEffect(() => { load() }, [load])
  useEffect(() => {
    const t = setInterval(load, 30_000)
    return () => clearInterval(t)
  }, [load])

  const closeStages: CloseStage[] = [
    { name: 'Document Ingestion', status: counts.docs > 0 ? 'done' : 'active',    pct: counts.docs > 0 ? 100 : 40 },
    { name: 'OCR & Extraction',   status: counts.docs > 2 ? 'done' : counts.docs > 0 ? 'active' : 'pending', pct: counts.docs > 2 ? 100 : 65 },
    { name: 'Reconciliation',     status: counts.recons > 0 ? 'done' : 'pending', pct: counts.recons > 0 ? 100 : 0 },
    { name: 'Exception Triage',   status: counts.exceptions === 0 ? 'done' : 'active', pct: counts.exceptions === 0 ? 100 : 62 },
    { name: 'Human Review',       status: counts.reviews === 0 ? 'done' : 'active', pct: counts.reviews === 0 ? 100 : 30 },
    { name: 'Evidence Binder',    status: 'pending', pct: 0 },
    { name: 'Period Close',       status: 'pending', pct: 0 },
  ]

  const overallPct = Math.round(
    closeStages.reduce((a, s) => a + s.pct, 0) / closeStages.length
  )

  const severityCounts = exceptions.reduce((acc, e) => {
    const sev = (e.severity || 'LOW').toUpperCase()
    acc[sev] = (acc[sev] || 0) + 1
    return acc
  }, {} as Record<string, number>)

  if (loading) return <SkeletonGrid />

  return (
    <div data-testid="dashboard-page" className="space-y-4">

      {/* ── Header row ── */}
      <div className="flex items-center justify-between gap-4">
        <div>
          <h1 className="text-lg font-bold text-white flex items-center gap-2" data-testid="dashboard-title">
            Pit Lane
            {liveRunning && (
              <span className="flex items-center gap-1 px-2 py-0.5 rounded-full bg-red-600/20 border border-red-500/30 text-red-400 text-[11px] font-mono animate-pulse">
                ● LIVE
              </span>
            )}
          </h1>
          <p className="text-xs text-gray-300 mt-0.5" data-testid="dashboard-subtitle">
            {health ? `${health.mode} · ${health.llm}` : 'Finance close overview'}
            {' · '}refreshed {lastRefresh.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </p>
        </div>
        <div className="flex items-center gap-2 flex-shrink-0">
          <button onClick={load}
            className="px-3 py-1.5 text-xs rounded-lg border border-[#2A2A3A] text-gray-500 hover:text-gray-300 hover:border-[#3A3A4A] transition font-mono">
            ↻
          </button>
          <Link to="/race-control"
            className="px-3 py-1.5 text-xs rounded-lg bg-red-600/10 border border-red-500/25 text-red-400 hover:bg-red-600/20 transition font-medium">
            🏎️ Race Control
          </Link>
        </div>
      </div>

      {/* ── KPI row ── */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
        <KpiCard label="Documents"      value={counts.docs}       icon="📄" accent="text-blue-400"   trend="up"                                    to="/documents"      sub="Ingested" />
        <KpiCard label="Reconciled"     value={counts.recons}     icon="⚖️" accent="text-green-400"  trend="up"                                    to="/reconciliation" sub={`${overallPct}% cycle`} />
        <KpiCard label="Exceptions"     value={counts.exceptions} icon="⚠️" accent="text-red-400"    trend={counts.exceptions > 0 ? 'down' : 'flat'} to="/exceptions"   sub="Pending resolution" />
        <KpiCard label="In Review"      value={counts.reviews}    icon="🔍" accent="text-yellow-400" trend="flat"                                  to="/review"         sub="Awaiting CFO" />
        <KpiCard label="Audit Events"   value={counts.audits}     icon="📋" accent="text-purple-400" trend="up"                                    to="/audit"          sub="This cycle" />
        <KpiCard label="Close Health"   value={`${overallPct}%`}  icon="🏁"
          accent={overallPct >= 80 ? 'text-green-400' : overallPct >= 50 ? 'text-yellow-400' : 'text-red-400'}
          trend="up" to="/close-scorecard"
          sub={overallPct === 100 ? '✅ All clear' : 'In progress'} />
      </div>

      {/* ── Middle row ── */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">

        {/* Close cycle progress */}
        <div className="rounded-xl border border-[#2A2A3A] bg-[#111118] p-4">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-sm font-semibold text-gray-300">Close Cycle · Mar 2026</h2>
            <span className="text-xs font-mono text-gray-400">{overallPct}%</span>
          </div>
          <div className="h-1.5 rounded-full bg-[#1E1E2E] overflow-hidden mb-4">
            <div
              className={`h-full rounded-full transition-all duration-700 ${
                overallPct >= 80 ? 'bg-green-500' : overallPct >= 50 ? 'bg-blue-500' : 'bg-red-500'
              }`}
              style={{ width: `${overallPct}%` }}
            />
          </div>
          <CloseProgress stages={closeStages} />
        </div>

        {/* Exceptions panel */}
        <div className="rounded-xl border border-[#2A2A3A] bg-[#111118] p-4">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-sm font-semibold text-gray-300">Active Exceptions</h2>
            <Link to="/exceptions" className="text-xs text-gray-400 hover:text-gray-400 transition">View all →</Link>
          </div>
          {exceptions.length > 0 ? (
            <>
              <SeverityBar counts={severityCounts} />
              <div className="mt-3 space-y-1.5">
                {exceptions.slice(0, 4).map((e, i) => {
                  const sev = (e.severity || 'LOW').toUpperCase()
                  return (
                    <div key={e.exception_id || e.id || i} className="flex items-center gap-2">
                      <span className={`text-[10px] px-1.5 py-0.5 rounded font-mono font-bold flex-shrink-0 ${
                        sev === 'CRITICAL' ? 'bg-red-900/40 text-red-400' :
                        sev === 'HIGH'     ? 'bg-orange-900/40 text-orange-400' :
                        sev === 'MEDIUM'   ? 'bg-yellow-900/40 text-yellow-400' :
                                             'bg-blue-900/40 text-blue-400'
                      }`}>{sev.slice(0, 4)}</span>
                      <span className="text-xs text-gray-500 truncate">
                        {e.description || e.message || 'Exception'}
                      </span>
                    </div>
                  )
                })}
              </div>
            </>
          ) : (
            <div className="flex flex-col items-center justify-center py-8 text-center">
              <span className="text-2xl mb-2">🟢</span>
              <p className="text-sm text-green-400 font-medium">All clear</p>
              <p className="text-xs text-gray-300">No exceptions flagged</p>
            </div>
          )}
        </div>

        {/* Activity feed */}
        <div className="rounded-xl border border-[#2A2A3A] bg-[#111118] p-4">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-sm font-semibold text-gray-300">Agent Activity</h2>
            <Link to="/audit" className="text-xs text-gray-400 hover:text-gray-400 transition">Full log →</Link>
          </div>
          <ActivityFeed events={activity} />
        </div>
      </div>

      {/* ── Status strip (health badges) ── */}
      {health && (
        <div className="flex flex-wrap gap-2">
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[11px] font-medium bg-green-900/20 border border-green-800/30 text-green-400">
            ● API {health.status.toUpperCase()}
          </span>
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[11px] font-medium bg-[#1A1A24] border border-[#2A2A3A] text-gray-500 font-mono">
            {health.project}
          </span>
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[11px] font-medium bg-[#1A1A24] border border-[#2A2A3A] text-gray-500 font-mono">
            MODE:{health.mode}
          </span>
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[11px] font-medium bg-[#1A1A24] border border-[#2A2A3A] text-gray-500 font-mono">
            LLM:{health.llm}
          </span>
        </div>
      )}

      {/* ── Quick actions ── */}
      <div className="rounded-xl border border-[#2A2A3A] bg-[#111118] p-4">
        <h2 className="text-sm font-semibold text-gray-500 mb-3 uppercase tracking-wider text-[11px]">Quick Actions</h2>
        <div className="flex flex-wrap gap-2">
          {[
            { to: '/documents',       label: '📄 Upload Document',        cls: 'border-blue-800/40 text-blue-400 hover:bg-blue-900/20' },
            { to: '/reconciliation',  label: '⚖️ Reconciliation',          cls: 'border-green-800/40 text-green-400 hover:bg-green-900/20' },
            { to: '/race-control',    label: '🏎️ Race Control',            cls: 'border-red-800/40 text-red-400 hover:bg-red-900/20' },
            { to: '/review',          label: '🔍 Review Queue',            cls: 'border-yellow-800/40 text-yellow-400 hover:bg-yellow-900/20' },
            { to: '/evidence-binder', label: '📦 Evidence Binder',         cls: 'border-purple-800/40 text-purple-400 hover:bg-purple-900/20' },
            { to: '/live-voice',      label: '🎙️ Ask LedgerBot',           cls: 'border-pink-800/40 text-pink-400 hover:bg-pink-900/20' },
            { to: '/close-scorecard', label: '🏁 Close Scorecard',         cls: 'border-gray-700/50 text-gray-400 hover:bg-gray-800/40' },
          ].map(a => (
            <Link key={a.to} to={a.to}
              className={`px-3.5 py-2 rounded-lg border text-xs font-medium transition ${a.cls}`}>
              {a.label}
            </Link>
          ))}
        </div>
      </div>

    </div>
  )
}
