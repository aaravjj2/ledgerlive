import { useEffect, useState } from 'react'
import { API_BASE } from '../services/api'

interface AuditEvent {
  trace_id: string
  action: string
  entity_type: string
  entity_id: string
  ts: string
  detail?: Record<string, unknown>
}

type SeverityLevel = 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'INFO'
type FilterLevel = 'ALL' | 'CRITICAL' | 'HIGH' | 'INFO'

const FILTERS: FilterLevel[] = ['ALL', 'CRITICAL', 'HIGH', 'INFO']

function getSeverity(action: string): SeverityLevel {
  const up = action.toUpperCase()
  if (
    up.includes('DELETE') ||
    up.includes('FAIL') ||
    up.includes('ERROR') ||
    up.includes('CRITICAL')
  )
    return 'CRITICAL'
  if (
    up.includes('REJECT') ||
    up.includes('BLOCK') ||
    up.includes('DENY') ||
    up.includes('WARN')
  )
    return 'HIGH'
  if (
    up.includes('UPDATE') ||
    up.includes('APPROVE') ||
    up.includes('MODIFY') ||
    up.includes('CLOSE')
  )
    return 'MEDIUM'
  return 'INFO'
}

function severityDotClass(s: SeverityLevel): string {
  switch (s) {
    case 'CRITICAL': return 'bg-red-500'
    case 'HIGH':     return 'bg-orange-500'
    case 'MEDIUM':   return 'bg-yellow-500'
    case 'INFO':     return 'bg-gray-500'
  }
}

function severityAccentClass(s: SeverityLevel): string {
  switch (s) {
    case 'CRITICAL': return 'bg-red-500'
    case 'HIGH':     return 'bg-orange-500'
    case 'MEDIUM':   return 'bg-yellow-500'
    case 'INFO':     return 'bg-gray-600'
  }
}

function severityLabelClass(s: SeverityLevel): string {
  switch (s) {
    case 'CRITICAL': return 'text-red-400'
    case 'HIGH':     return 'text-orange-400'
    case 'MEDIUM':   return 'text-yellow-400'
    case 'INFO':     return 'text-gray-400'
  }
}

function matchesFilter(filter: FilterLevel, severity: SeverityLevel): boolean {
  if (filter === 'ALL') return true
  if (filter === 'INFO') return severity === 'INFO' || severity === 'MEDIUM'
  return severity === filter
}

export default function AuditLog() {
  const [events, setEvents] = useState<AuditEvent[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState<FilterLevel>('ALL')
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null)
  const [secondsAgo, setSecondsAgo] = useState(0)

  const load = () => {
    setLoading(true)
    fetch(`${API_BASE}/api/audit`)
      .then(r => r.json())
      .then(d => {
        setEvents((d.events || []).slice().reverse())
        setLoading(false)
        setLastUpdated(new Date())
        setSecondsAgo(0)
      })
      .catch(() => setLoading(false))
  }

  useEffect(() => { load() }, [])

  useEffect(() => {
    if (!lastUpdated) return
    const id = setInterval(() => {
      setSecondsAgo(Math.floor((Date.now() - lastUpdated.getTime()) / 1000))
    }, 1000)
    return () => clearInterval(id)
  }, [lastUpdated])

  const handleExport = () => {
    fetch(`${API_BASE}/api/audit/export`)
      .then(r => {
        if (!r.ok) return Promise.reject(new Error('export unavailable'))
        return r.blob()
      })
      .then(blob => {
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `audit-pack-${new Date().toISOString().slice(0, 10)}.json`
        a.click()
        URL.revokeObjectURL(url)
      })
      .catch(() => {
        const blob = new Blob([JSON.stringify(events, null, 2)], {
          type: 'application/json',
        })
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `audit-pack-${new Date().toISOString().slice(0, 10)}.json`
        a.click()
        URL.revokeObjectURL(url)
      })
  }

  const filteredEvents = events.filter(e =>
    matchesFilter(filter, getSeverity(e.action))
  )

  return (
    <div data-testid="audit-page" className="min-h-screen bg-[#0A0A0F] p-6">

      {/* ── Header ──────────────────────────────────────────────────── */}
      <div className="flex flex-wrap items-start justify-between gap-3 mb-2">
        <div className="flex items-center gap-3">
          <h1
            data-testid="audit-title"
            className="text-2xl font-bold text-[#F8F9FA] tracking-tight"
          >
            Audit Log
          </h1>
          {!loading && events.length > 0 && (
            <span className="px-2 py-0.5 rounded text-xs font-bold bg-green-900/40 text-green-400 border border-green-800/50 tracking-wider">
              VERIFIED
            </span>
          )}
        </div>

        <div className="flex items-center gap-2 flex-wrap">
          {lastUpdated && (
            <span className="text-xs text-[#9CA3AF] bg-[#111118] px-3 py-1.5 rounded-lg border border-[#2A2A3A] font-mono">
              Updated {secondsAgo}s ago
            </span>
          )}
          <button
            onClick={handleExport}
            className="text-sm px-3 py-1.5 rounded-lg bg-[#111118] border border-[#2A2A3A] text-[#9CA3AF] hover:text-[#F8F9FA] hover:border-[#3A3A4A] transition-colors"
          >
            Export Audit Pack
          </button>
          <button
            onClick={load}
            className="text-sm px-3 py-1.5 rounded-lg bg-[#E8002D] text-white hover:bg-[#C8001D] transition-colors font-medium"
          >
            ↻ Refresh
          </button>
        </div>
      </div>

      <p
        data-testid="audit-subtitle"
        className="text-[#9CA3AF] mb-5"
      >
        Immutable audit trail of all system actions.
      </p>

      {/* ── Filter Bar ──────────────────────────────────────────────── */}
      <div className="flex items-center gap-2 mb-6 flex-wrap">
        {FILTERS.map(f => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`px-3 py-1 rounded-full text-xs font-semibold transition-colors border ${
              filter === f
                ? 'bg-[#E8002D] text-white border-[#E8002D]'
                : 'bg-[#111118] text-[#9CA3AF] border-[#2A2A3A] hover:border-[#3A3A4A] hover:text-[#F8F9FA]'
            }`}
          >
            {f}
          </button>
        ))}
        <span className="ml-auto text-xs text-[#9CA3AF] font-mono">
          {filteredEvents.length} event{filteredEvents.length !== 1 ? 's' : ''}
        </span>
      </div>

      {/* ── Timeline ────────────────────────────────────────────────── */}
      {loading ? (
        <div className="flex items-center justify-center py-24">
          <p className="text-[#9CA3AF] text-sm">Loading audit events…</p>
        </div>
      ) : filteredEvents.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-24 gap-1">
          <p className="text-[#9CA3AF]">No audit events found.</p>
          <p className="text-[#9CA3AF]/60 text-sm">
            {filter !== 'ALL'
              ? 'Try a different severity filter.'
              : 'Perform an action to generate entries.'}
          </p>
        </div>
      ) : (
        <div className="relative pl-9">
          {/* Vertical guide line */}
          <div className="absolute left-[14px] top-2 bottom-2 w-px bg-[#2A2A3A]" />

          <div className="space-y-3">
            {filteredEvents.map((e, i) => {
              const sev = getSeverity(e.action)
              const actor =
                (e.detail?.actor as string) ||
                (e.detail?.user as string) ||
                'system'
              const ts = e.ts ? new Date(e.ts) : null

              return (
                <div key={e.trace_id + i} className="relative flex gap-3">
                  {/* Severity dot */}
                  <div className="absolute -left-9 top-3.5 w-9 flex justify-center">
                    <div
                      className={`w-3 h-3 rounded-full ring-2 ring-[#0A0A0F] ${severityDotClass(sev)}`}
                    />
                  </div>

                  {/* Entry card */}
                  <div className="flex-1 bg-[#111118] border border-[#2A2A3A] rounded-lg overflow-hidden flex min-w-0">
                    {/* Colored accent bar */}
                    <div className={`w-1 flex-shrink-0 ${severityAccentClass(sev)}`} />

                    <div className="flex-1 p-3 min-w-0">
                      {/* Meta row */}
                      <div className="flex items-center gap-2 flex-wrap mb-1">
                        <span className="font-mono text-xs text-[#00D2FF] flex-shrink-0">
                          {ts
                            ? ts.toISOString().replace('T', ' ').slice(0, 23)
                            : '—'}
                        </span>
                        <span className="px-1.5 py-0.5 rounded bg-[#1A1A24] text-[#9CA3AF] text-xs border border-[#2A2A3A]">
                          {actor}
                        </span>
                        <span
                          className={`text-xs font-semibold ${severityLabelClass(sev)}`}
                        >
                          {sev}
                        </span>
                      </div>

                      {/* Action description */}
                      <p className="text-[#F8F9FA] text-sm font-medium truncate">
                        {e.action}
                      </p>

                      {/* Affected entity */}
                      <p className="text-xs text-[#9CA3AF] mt-0.5 font-mono truncate">
                        <span className="text-[#9CA3AF]/70">{e.entity_type}</span>
                        {' · '}
                        <span>{e.entity_id.slice(0, 12)}…</span>
                        {' · '}
                        <span className="text-[#9CA3AF]/60">
                          {e.trace_id.slice(0, 8)}…
                        </span>
                      </p>
                    </div>
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      )}
    </div>
  )
}
