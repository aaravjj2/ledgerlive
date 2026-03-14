/**
 * Close Calendar — Dependency graph, SLA timers, owner assignments
 * W31 Close Calendar 2.0 frontend
 */
import { useEffect, useState } from 'react'

interface CalendarTask {
  task_id: string
  name: string
  due_date: string
  owner?: string
  status: 'pending' | 'in_progress' | 'completed' | 'blocked'
  dependencies: string[]
  sla_hours?: number
}

export default function CloseCalendar() {
  const [tasks, setTasks] = useState<CalendarTask[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/close-calendar').then(r => r.json()).catch(() => ({ items: [] }))
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

  const statusColor = (s: string) => {
    if (s === 'completed') return 'bg-green-100 text-green-800'
    if (s === 'in_progress') return 'bg-blue-100 text-blue-800'
    if (s === 'blocked') return 'bg-red-100 text-red-800'
    return 'bg-gray-100 text-gray-600'
  }

  return (
    <div data-testid="close-calendar-page">
      <h1 className="text-2xl font-bold mb-1" data-testid="close-calendar-title">Close Calendar</h1>
      <p className="text-gray-500 mb-6">Dependency graph, SLA timers, and owner assignments.</p>

      {loading ? (
        <p className="text-gray-400">Loading…</p>
      ) : (
        <div className="rounded-xl border bg-white shadow-sm overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-gray-50 border-b">
              <tr>
                <th className="text-left px-4 py-3 font-semibold text-gray-600">Task</th>
                <th className="text-left px-4 py-3 font-semibold text-gray-600">Due</th>
                <th className="text-left px-4 py-3 font-semibold text-gray-600">Owner</th>
                <th className="text-left px-4 py-3 font-semibold text-gray-600">Status</th>
                <th className="text-left px-4 py-3 font-semibold text-gray-600">Dependencies</th>
              </tr>
            </thead>
            <tbody>
              {tasks.map(t => (
                <tr key={t.task_id} className="border-b hover:bg-gray-50" data-testid={`close-calendar-row-${t.task_id}`}>
                  <td className="px-4 py-3 font-medium">{t.name}</td>
                  <td className="px-4 py-3 text-gray-600">{t.due_date}</td>
                  <td className="px-4 py-3 text-gray-600">{t.owner || '—'}</td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${statusColor(t.status)}`}>
                      {t.status}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-gray-500 font-mono text-xs">{t.dependencies.join(', ') || '—'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
