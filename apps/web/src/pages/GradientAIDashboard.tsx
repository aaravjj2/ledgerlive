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

const OCR_MOCK = {
  vendor:        { label: 'Vendor Name',      value: 'ACME Supplies Ltd.',       confidence: 98 },
  invoice_no:    { label: 'Invoice Number',   value: 'INV-2026-00842',           confidence: 99 },
  date:          { label: 'Invoice Date',     value: 'March 10, 2026',           confidence: 97 },
  total:         { label: 'Total Amount',     value: '$14,500.00',               confidence: 96 },
  tax:           { label: 'Tax (8.5%)',       value: '$1,189.75',                confidence: 94 },
  po:            { label: 'PO Reference',     value: 'PO-2026-0312',             confidence: 91 },
}

function ConfidenceBar({ pct }: { pct: number }) {
  const color = pct >= 95 ? 'bg-green-500' : pct >= 85 ? 'bg-yellow-500' : 'bg-red-500'
  return (
    <div className="flex items-center gap-2">
      <div className="flex-1 h-1.5 bg-[#2A2A3A] rounded-full overflow-hidden">
        <div className={`h-full ${color} rounded-full transition-all`} style={{ width: `${pct}%` }} />
      </div>
      <span className={`text-xs font-mono w-10 text-right ${pct >= 95 ? 'text-green-400' : pct >= 85 ? 'text-yellow-400' : 'text-red-400'}`}>
        {pct}%
      </span>
    </div>
  )
}

export default function GradientAIDashboard() {
  const [trainingJobs, setTrainingJobs] = useState<TrainingJob[]>([])
  const [inferenceRuns, setInferenceRuns] = useState<InferenceRun[]>([])
  const [loading, setLoading] = useState(true)
  const [ocrTab, setOcrTab] = useState<'extracted' | 'raw'>('extracted')

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
      {/* Header */}
      <div className="flex items-center justify-between flex-wrap gap-3">
        <div>
          <h1 className="text-2xl font-bold" data-testid="gradient-title">Gradient AI Dashboard</h1>
          <p className="text-gray-500 text-sm mt-1">
            DigitalOcean Gradient™ AI — Model training, inference, deployment for finance close ML
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span className="px-3 py-1 bg-blue-900/30 border border-blue-500/30 text-blue-300 text-xs rounded-lg font-medium">
            🔵 Powered by DigitalOcean Gradient AI
          </span>
          <button
            onClick={load}
            disabled={loading}
            className="px-4 py-2 bg-red-600 text-white rounded-lg text-sm font-medium hover:bg-red-700 disabled:opacity-50"
          >
            {loading ? 'Loading…' : '↻ Refresh'}
          </button>
        </div>
      </div>

      {/* Ticker */}
      <TickerBar items={tickerItems} dataTestId="gradient-ticker" />

      {/* OCR Demo — Primary showcase */}
      <div className="rounded-xl border border-[#2A2A3A] bg-[#111118] overflow-hidden">
        <div className="flex items-center justify-between px-4 py-3 border-b border-[#2A2A3A] bg-[#1A1A24]">
          <h2 className="font-semibold text-gray-200">OCR Document Intelligence</h2>
          <span className="text-xs text-gray-500 bg-[#0A0A0F] border border-[#2A2A3A] px-2 py-0.5 rounded">
            Live OCR · 94.2% avg confidence
          </span>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-0">
          {/* Left: document preview */}
          <div className="p-4 border-b lg:border-b-0 lg:border-r border-[#2A2A3A]">
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs text-gray-400 uppercase tracking-wide font-semibold">Source Document</span>
              <span className="text-xs text-green-400 bg-green-900/40 px-2 py-0.5 rounded">✓ Processed</span>
            </div>
            {/* Mock document preview */}
            <div className="bg-[#0A0A0F] border border-[#2A2A3A] rounded-lg p-4 font-mono text-xs text-gray-400 space-y-1.5">
              <div className="text-gray-200 font-bold text-sm">ACME SUPPLIES LTD.</div>
              <div className="text-gray-500">123 Business Park, Suite 400</div>
              <div className="border-t border-[#2A2A3A] my-2" />
              <div className="flex justify-between">
                <span>Invoice #</span><span className="text-[#00D2FF]">INV-2026-00842</span>
              </div>
              <div className="flex justify-between">
                <span>Date</span><span>March 10, 2026</span>
              </div>
              <div className="flex justify-between">
                <span>PO Reference</span><span>PO-2026-0312</span>
              </div>
              <div className="border-t border-[#2A2A3A] my-2" />
              <div className="space-y-1">
                <div className="flex justify-between text-gray-500">
                  <span>Professional Services</span><span>$12,000.00</span>
                </div>
                <div className="flex justify-between text-gray-500">
                  <span>Software License</span><span>$1,310.25</span>
                </div>
                <div className="flex justify-between text-gray-500">
                  <span>Tax (8.5%)</span><span>$1,189.75</span>
                </div>
              </div>
              <div className="border-t border-[#2A2A3A] my-1" />
              <div className="flex justify-between text-gray-100 font-bold">
                <span>TOTAL</span><span className="text-red-400">$14,500.00</span>
              </div>
            </div>
          </div>

          {/* Right: extracted data */}
          <div className="p-4">
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs text-gray-400 uppercase tracking-wide font-semibold">Extracted Fields</span>
              <div className="flex gap-1">
                {(['extracted', 'raw'] as const).map(t => (
                  <button
                    key={t}
                    onClick={() => setOcrTab(t)}
                    className={`text-xs px-2 py-1 rounded transition-colors ${
                      ocrTab === t ? 'bg-red-600 text-white' : 'bg-[#1A1A24] text-gray-400 hover:bg-[#2A2A3A]'
                    }`}
                  >
                    {t === 'extracted' ? 'Fields' : 'Raw'}
                  </button>
                ))}
              </div>
            </div>

            {ocrTab === 'extracted' ? (
              <div className="space-y-3">
                {Object.entries(OCR_MOCK).map(([key, field]) => (
                  <div key={key}>
                    <div className="flex justify-between items-baseline mb-1">
                      <span className="text-xs text-gray-500">{field.label}</span>
                      <span className="text-sm text-gray-100 font-mono">{field.value}</span>
                    </div>
                    <ConfidenceBar pct={field.confidence} />
                  </div>
                ))}
              </div>
            ) : (
              <pre className="bg-[#0A0A0F] text-[#00D2FF] text-xs font-mono p-3 rounded-lg overflow-auto h-48 leading-relaxed">
{`VENDOR: ACME SUPPLIES LTD.
ADDRESS: 123 Business Park
INVOICE_NO: INV-2026-00842
DATE: 2026-03-10
LINE_ITEMS:
  - Professional Services: $12,000.00
  - Software License: $1,310.25
TAX_RATE: 8.5%
TAX_AMOUNT: $1,189.75
TOTAL: $14,500.00
PO_REF: PO-2026-0312`}
              </pre>
            )}

            <div className="mt-3 pt-3 border-t border-[#2A2A3A] flex items-center gap-2">
              <span className="text-xs text-gray-400">AI confidence:</span>
              <div className="flex-1 h-1 bg-[#2A2A3A] rounded-full overflow-hidden">
                <div className="h-full bg-green-500 rounded-full" style={{ width: '94.2%' }} />
              </div>
              <span className="text-xs text-green-400 font-mono">94.2%</span>
            </div>
          </div>
        </div>
      </div>

      {/* Training + Inference */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="rounded-xl border border-[#2A2A3A] bg-[#111118] p-4">
          <h2 className="text-lg font-semibold mb-3 text-gray-200">Training Jobs</h2>
          {trainingJobs.length === 0 ? (
            <p className="text-gray-500 text-sm">No training jobs. Start one via API.</p>
          ) : (
            <div className="space-y-2">
              {trainingJobs.slice(0, 8).map(j => (
                <div key={j.job_id} className="flex items-center justify-between py-2 border-b border-[#2A2A3A] last:border-0">
                  <span className="font-mono text-xs text-gray-300">{j.model_name}</span>
                  <div className="flex items-center gap-2">
                    <div className="w-24 h-1.5 bg-[#2A2A3A] rounded overflow-hidden">
                      <div className="h-full bg-green-500" style={{ width: `${j.progress_pct}%` }} />
                    </div>
                    <StatusBadge status={j.status} />
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="rounded-xl border border-[#2A2A3A] bg-[#111118] p-4">
          <h2 className="text-lg font-semibold mb-3 text-gray-200">Inference Runs</h2>
          {inferenceRuns.length === 0 ? (
            <p className="text-gray-500 text-sm">No inference runs yet.</p>
          ) : (
            <div className="space-y-2">
              {inferenceRuns.slice(0, 8).map(r => (
                <div key={r.run_id} className="flex items-center justify-between py-2 border-b border-[#2A2A3A] last:border-0 text-sm">
                  <span className="font-mono text-xs text-gray-400">{r.run_id.slice(0, 8)}…</span>
                  <span className={r.success ? 'text-green-400' : 'text-red-400'}>{r.latency_ms}ms</span>
                  <span className={r.success ? 'text-green-400' : 'text-red-400'}>{r.success ? '✓' : '✗'}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Heatmap */}
      {heatmapData.length > 0 && (
        <div>
          <h2 className="text-lg font-semibold mb-3 text-gray-200">Training Progress Heatmap</h2>
          <Heatmap
            cells={heatmapData.map(d => ({ id: d.id, label: d.label, value: d.value, status: d.status === 'completed' ? 'ok' : d.status === 'failed' ? 'critical' : 'warning' }))}
            dataTestId="gradient-heatmap"
          />
        </div>
      )}

      {/* DO hackathon banner */}
      <div className="rounded-xl border border-amber-500/30 bg-amber-900/20 p-4">
        <h3 className="font-semibold text-amber-300 mb-1">🏆 DigitalOcean Gradient™ AI Hackathon</h3>
        <p className="text-sm text-amber-400">
          This dashboard showcases full-stack AI: GPU-backed training, flexible inference, seamless deployment.
          Integrates with LedgerLive finance close for exception classification, accrual suggestions, and audit automation.
        </p>
      </div>
    </div>
  )
}
