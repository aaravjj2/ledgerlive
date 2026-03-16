/**
 * Close Calendar — Dependency graph, SLA timers, owner assignments
 * W31 Close Calendar 2.0 frontend
 */
import { useEffect, useState } from 'react'
import { API_BASE } from '../services/api'

interface CalendarTask {
  task_id: string
  name: string
  due_date: string
  owner?: string
  status: 'pending' | 'in_progress' | 'completed' | 'blocked'
  dependencies: string[]
  sla_hours?: number
}

const STATUS_STYLE: Record<string, { pill: string; dot: string; label: string }> = {
  completed:   { pill: 'bg-green-900/40 text-green-300 border border-green-500/20', dot: 'bg-green-500', label: 'Completed' },
  in_progress: { pill: 'bg-blue-900/40 text-blue-400 border border-blue-500/20',   dot: 'bg-blue-400 animate-pulse', label: 'In Progress' },
  blocked:     { pill: 'bg-red-900/40 text-red-400 border border-red-500/20',       dot: 'bg-red-500', label: 'Blocked' },
  pending:     { pill: 'bg-[#1A1A24] text-gray-400 border border-[#2A2A3A]',        dot: 'bg-gray-600', label: 'Pending' },
}

function SlaCountdown({ dueDate }: { dueDate: string }) {
  const due = new Date(dueDate + 'T23:59:00')
  const now = new Date()
  const hoursLeft = Math.round((due.getTime() - now.getTime()) / 3600000)
  if (hoursLeft < 0) return <span className="text-xs text-red-400 font-mono">OVERDUE</span>
  if (hoursLeft < 24) return <span className="text-xs text-amber-400 font-mono animate-pulse">{hoursLeft}h left</span>
  return null
}

function TaskPill({ task, allTasks }: { task: CalendarTask, allTasks: CalendarTask[] }) {
  const [expanded, setExpanded] = useState(false)
  const style = STATUS_STYLE[task.status] ?? STATUS_STYLE.pending
  const depNames = task.dependencies.map(d => allTasks.find(t => t.task_id === d)?.name ?? d)

  return (
    <div
      className={`rounded-xl border bg-[#111118] overflow-hidden transition-all`}
      data-testid={`close-calendar-row-${task.task_id}`}
    >
      <button
        className="w-full flex items-center gap-3 px-4 py-3 text-left hover:bg-[#1A1A24] transition-colors"
        onClick={() => setExpanded(e => !e)}
      >
        {/* Status dot */}
        <div className={`w-2.5 h-2.5 rounded-full shrink-0 ${style.dot}`} />

        {/* Task name */}
        <div className="flex-1 min-w-0">
          <span className={`font-medium text-sm ${task.status === 'completed' ? 'line-through text-gray-500' : 'text-gray-100'}`}>
            {task.name}
          </span>
        </div>

        {/* Due date + SLA */}
        <div className="flex items-center gap-2 shrink-0">
          <SlaCountdown dueDate={task.due_date} />
          <span className="text-xs text-gray-500 font-mono">{task.due_date.slice(5)}</span>
        </div>

        {/* Owner badge */}
        {task.owner && (
          <span className="text-xs bg-[#1A1A24] border border-[#2A2A3A] text-gray-400 px-2 py-0.5 rounded-full shrink-0 hidden sm:block">
            {task.owner}
          </span>
        )}

        {/* Status badge */}
        <span className={`px-2 py-0.5 rounded-full text-xs font-medium shrink-0 ${style.pill}`}>
          {style.label}
        </span>

        {/* Expand chevron */}
        <span className={`text-gray-400 text-xs transition-transform shrink-0 ${expanded ? 'rotate-90' : ''}`}>
          ›
        </span>
      </button>

      {/* Expanded detail */}
      {expanded && (
        <div className="px-4 pb-3 border-t border-[#2A2A3A] bg-[#0D0D14]">
          <div className="grid grid-cols-2 gap-3 pt-3 text-sm">
            <div>
              <p className="text-xs text-gray-500 mb-1">Owner</p>
              <p className="text-gray-300">{task.owner || '—'}</p>
            </div>
            <div>
              <p className="text-xs text-gray-500 mb-1">Due Date</p>
              <p className="text-gray-300 font-mono">{task.due_date}</p>
            </div>
            {depNames.length > 0 && (
              <div className="col-span-2">
                <p className="text-xs text-gray-500 mb-1">Dependencies</p>
                <div className="flex flex-wrap gap-1">
                  {depNames.map((d, i) => (
                    <span key={i} className="text-xs bg-[#1A1A24] border border-[#2A2A3A] text-gray-400 px-2 py-0.5 rounded">
                      → {d}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default function CloseCalendar() {
  const [tasks, setTasks] = useState<CalendarTask[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState<string>('all')

  useEffect(() => {
    fetch(`${API_BASE}/api/close-calendar`)
      .then(r => r.json())
      .catch(() => ({ items: [] }))
      .then(d => {
        setTasks(d.items || [
          { task_id: 't1', name: 'Sub-ledger feeds', due_date: '2026-03-05', owner: 'Finance', status: 'completed', dependencies: [] },
          { task_id: 't2', name: 'AP matching', due_date: '2026-03-07', owner: 'AP Team', status: 'in_progress', dependencies: ['t1'] },
          { task_id: 't3', name: 'Cutoff review', due_date: '2026-03-08', owner: 'Controller', status: 'pending', dependencies: ['t2'] },
          { task_id: 't4', name: 'IC elimination', due_date: '2026-03-09', owner: 'Consol', status: 'pending', dependencies: ['t3'] },
          { task_id: 't5', name: 'Exception triage', due_date: '2026-03-10', owner: 'Close', status: 'pending', dependencies: ['t4'] },
        ])
      })
      .finally(() => setLoading(false))
  }, [])

  const filtered = tasks.filter(t => filter === 'all' || t.status === filter)

  const counts = {
    all: tasks.length,
    completed: tasks.filter(t => t.status === 'completed').length,
    in_progress: tasks.filter(t => t.status === 'in_progress').length,
    blocked: tasks.filter(t => t.status === 'blocked').length,
    pending: tasks.filter(t => t.status === 'pending').length,
  }

  const FILTERS = [
    { key: 'all',         label: 'All',        count: counts.all },
    { key: 'in_progress', label: 'In Progress', count: counts.in_progress },
    { key: 'pending',     label: 'Pending',     count: counts.pending },
    { key: 'blocked',     label: 'Blocked',     count: counts.blocked },
    { key: 'completed',   label: 'Done',        count: counts.completed },
  ]

  return (
    <div data-testid="close-calendar-page" className="space-y-5">
      {/* Header */}
      <div className="flex items-start justify-between flex-wrap gap-3">
        <div>
          <h1 className="text-2xl font-bold" data-testid="close-calendar-title">Close Calendar</h1>
          <p className="text-gray-500 text-sm mt-1">March 2026 · Dependency graph, SLA timers, and owner assignments.</p>
        </div>
        <div className="flex items-center gap-2 text-sm">
          <div className="flex items-center gap-1 px-3 py-1.5 bg-green-900/20 border border-green-500/30 rounded-lg">
            <span className="text-green-400 font-bold">{counts.completed}</span>
            <span className="text-green-400 text-xs">completed</span>
          </div>
          <div className="flex items-center gap-1 px-3 py-1.5 bg-blue-900/20 border border-blue-500/30 rounded-lg">
            <span className="text-blue-400 font-bold">{counts.in_progress}</span>
            <span className="text-blue-400 text-xs">in progress</span>
          </div>
          {counts.blocked > 0 && (
            <div className="flex items-center gap-1 px-3 py-1.5 bg-red-900/20 border border-red-500/30 rounded-lg">
              <span className="text-red-400 font-bold">{counts.blocked}</span>
              <span className="text-red-400 text-xs">blocked</span>
            </div>
          )}
        </div>
      </div>

      {/* Filter tabs */}
      <div className="flex gap-2 flex-wrap">
        {FILTERS.map(f => (
          <button
            key={f.key}
            onClick={() => setFilter(f.key)}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
              filter === f.key
                ? 'bg-red-600 text-white'
                : 'bg-[#1A1A24] text-gray-400 border border-[#2A2A3A] hover:bg-[#2A2A3A]'
            }`}
          >
            {f.label}
            <span className={`text-xs px-1 rounded ${filter === f.key ? 'bg-red-800 text-red-200' : 'bg-[#0A0A0F] text-gray-500'}`}>
              {f.count}
            </span>
          </button>
        ))}
      </div>

      {/* Task list */}
      {loading ? (
        <div className="space-y-2">
          {[1, 2, 3].map(i => (
            <div key={i} className="h-14 rounded-xl bg-[#111118] border border-[#2A2A3A] animate-pulse" />
          ))}
        </div>
      ) : (
        <div className="space-y-2">
          {filtered.map(task => (
            <TaskPill key={task.task_id} task={task} allTasks={tasks} />
          ))}
          {filtered.length === 0 && (
            <div className="text-center py-12 text-gray-500 text-sm">
              No {filter === 'all' ? '' : filter.replace('_', ' ')} tasks.
            </div>
          )}
        </div>
      )}
    </div>
  )
}
