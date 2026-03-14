/**
 * Gradient AI Dashboard — DigitalOcean Gradient™ AI Hackathon
 * Full-stack AI: model training, inference, deployment.
 * Showcases GPU-powered workflows for finance close ML.
 */
import { useEffect, useState, useCallback } from 'react'
import { apiGet } from '../services/api'
import { TickerBar } from '../components/TickerBar'
import { Heatmap } from '../components/Heatmap'
import { StatusBadge } from '../components/StatusBadge'

interface TrainingJob {
  job_id: string
  model_name: string
  status: string
  progress_pct: number
  gpu_hours: number
  created_at: string
}

interface InferenceRun {
  run_id: string
  model_id: string
  latency_ms: number
  success: boolean
  timestamp: string
}

export default function GradientAIDashboard() {
  const [trainingJobs, setTrainingJobs] = useState<TrainingJob[]>([])
  const [inferenceRuns, setInferenceRuns] = useState<InferenceRun[]>([])
  const [loading, setLoading] = useState(true)

  const load = useCallback(async () => {
    setLoading(true)
    try {
      const [t, i] = await Promise.all([
        apiGet<{ items?: TrainingJob[] }>('/api/gradient-training').catch(() => ({ items: [] })),
        apiGet<{ items?: InferenceRun[] }>('/api/gradient-inference').catch(() => ({ items: [] })),
      ])
      setTrainingJobs(t?.items ?? [])
      setInferenceRuns(i?.items ?? [])
    } catch {
      setTrainingJobs([])
      setInferenceRuns([])
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { load() }, [load])

  const tickerItems = [
    { id: 'jobs', label: 'Training Jobs', value: trainingJobs.length },
    { id: 'runs', label: 'Inference Runs', value: inferenceRuns.length },
    { id: 'latency', label: 'Avg Latency', value: inferenceRuns.length ? `${Math.round(inferenceRuns.reduce((a, r) => a + r.latency_ms, 0) / inferenceRuns.length)}ms` : '—' },
    { id: 'success', label: 'Success Rate', value: inferenceRuns.length ? `${Math.round(100 * inferenceRuns.filter(r => r.success).length / inferenceRuns.length)}%` : '—' },
  ]

  const heatmapData = trainingJobs.slice(0, 12).map(j => ({
    id: j.job_id,
    label: j.model_name.slice(0, 12),
    value: j.progress_pct,
    status: j.status,
  }))

  return (
    <div data-testid="gradient-ai-dashboard" className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold" data-testid="gradient-title">Gradient AI Dashboard</h1>
          <p className="text-gray-500 text-sm mt-1">
            DigitalOcean Gradient™ AI — Model training, inference, deployment for finance close ML
          </p>
        </div>
        <button
          onClick={load}
          disabled={loading}
          className="px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 disabled:opacity-50"
        >
          {loading ? 'Loading…' : '↻ Refresh'}
        </button>
      </div>

      <TickerBar items={tickerItems} dataTestId="gradient-ticker" />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="rounded-xl border bg-slate-900 text-white p-4">
          <h2 className="text-lg font-semibold mb-3">Training Jobs</h2>
          {trainingJobs.length === 0 ? (
            <p className="text-slate-400 text-sm">No training jobs. Start one via API.</p>
          ) : (
            <div className="space-y-2">
              {trainingJobs.slice(0, 8).map(j => (
                <div key={j.job_id} className="flex items-center justify-between py-2 border-b border-slate-700 last:border-0">
                  <span className="font-mono text-xs">{j.model_name}</span>
                  <div className="flex items-center gap-2">
                    <div className="w-24 h-1.5 bg-slate-700 rounded overflow-hidden">
                      <div className="h-full bg-emerald-500" style={{ width: `${j.progress_pct}%` }} />
                    </div>
                    <StatusBadge status={j.status} />
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="rounded-xl border bg-slate-900 text-white p-4">
          <h2 className="text-lg font-semibold mb-3">Inference Runs</h2>
          {inferenceRuns.length === 0 ? (
            <p className="text-slate-400 text-sm">No inference runs yet.</p>
          ) : (
            <div className="space-y-2">
              {inferenceRuns.slice(0, 8).map(r => (
                <div key={r.run_id} className="flex items-center justify-between py-2 border-b border-slate-700 last:border-0 text-sm">
                  <span className="font-mono text-xs">{r.run_id.slice(0, 8)}…</span>
                  <span className={r.success ? 'text-emerald-400' : 'text-red-400'}>{r.latency_ms}ms</span>
                  <span className={r.success ? 'text-emerald-400' : 'text-red-400'}>{r.success ? '✓' : '✗'}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      <div>
        <h2 className="text-lg font-semibold mb-3">Training Progress Heatmap</h2>
        <Heatmap
          cells={heatmapData.map(d => ({ id: d.id, label: d.label, value: d.value, status: d.status === 'completed' ? 'ok' : d.status === 'failed' ? 'critical' : 'warning' }))}
          dataTestId="gradient-heatmap"
        />
      </div>

      <div className="rounded-xl border bg-amber-50 border-amber-200 p-4">
        <h3 className="font-semibold text-amber-800 mb-2">DigitalOcean Gradient™ AI Hackathon</h3>
        <p className="text-sm text-amber-700">
          This dashboard showcases full-stack AI: GPU-backed training, flexible inference, seamless deployment.
          Integrates with LedgerLive finance close for exception classification, accrual suggestions, and audit automation.
        </p>
      </div>
    </div>
  )
}
