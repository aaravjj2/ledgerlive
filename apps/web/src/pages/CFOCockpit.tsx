/**
 * CFO Cockpit — Executive finance metrics and scenario pack.
 * Integrates /api/cfo/cockpit, /api/cfo/scenario, /api/cfo/story-mode.
 */
import { useEffect, useState, useCallback } from 'react'

interface CockpitMetric {
  metric_id: string
  label: string
  value: number | string
  unit?: string
  trend?: 'up' | 'down' | 'flat'
  health?: 'green' | 'yellow' | 'red'
}

interface ScenarioPack {
  scenario_id: string
  name: string
  description?: string
  metrics: Record<string, number>
  created_at: string
}

interface StoryModeResult {
  story_id: string
  narrative: string
  highlights: string[]
  metrics_snapshot: Record<string, number>
}

export default function CFOCockpit() {
  const [metrics, setMetrics] = useState<CockpitMetric[]>([])
  const [scenarios, setScenarios] = useState<ScenarioPack[]>([])
  const [story, setStory] = useState<StoryModeResult | null>(null)
  const [loading, setLoading] = useState(true)
  const [storyLoading, setStoryLoading] = useState(false)

  const loadCockpit = useCallback(() => {
    Promise.all([
      fetch('/api/cfo/cockpit').then(r => r.json()),
      fetch('/api/cfo/scenario').then(r => r.json()),
    ]).then(([cockpit, scenario]) => {
      setMetrics(cockpit.metrics || [])
      setScenarios(scenario.scenarios || scenario.items || [])
      setLoading(false)
    }).catch(() => setLoading(false))
  }, [])

  useEffect(() => { loadCockpit() }, [loadCockpit])

  const runStoryMode = async () => {
    setStoryLoading(true)
    setStory(null)
    try {
      const r = await fetch('/api/cfo/story-mode', { method: 'POST' })
      const j = await r.json()
      setStory(j)
    } catch {
      setStory({ story_id: 'err', narrative: 'Failed to load story.', highlights: [], metrics_snapshot: {} })
    }
    setStoryLoading(false)
  }

  const healthColor = (h?: string) => {
    if (h === 'green') return 'bg-green-100 text-green-800 border-green-300'
    if (h === 'yellow') return 'bg-yellow-100 text-yellow-800 border-yellow-300'
    if (h === 'red') return 'bg-red-100 text-red-800 border-red-300'
    return 'bg-gray-100 text-gray-800 border-gray-300'
  }

  const trendIcon = (t?: string) => {
    if (t === 'up') return '↑'
    if (t === 'down') return '↓'
    return '→'
  }

  return (
    <div data-testid="cfo-cockpit-page" className="pb-10">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold" data-testid="cfo-cockpit-title">CFO Cockpit</h1>
          <p className="text-gray-500 text-sm mt-1">Executive metrics, scenario packs, and narrative story mode.</p>
        </div>
        <div className="flex gap-2">
          <button
            data-testid="cfo-cockpit-refresh"
            onClick={loadCockpit}
            className="px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700"
          >
            ↻ Refresh
          </button>
          <button
            data-testid="cfo-story-mode"
            onClick={runStoryMode}
            disabled={storyLoading}
            className="px-4 py-2 bg-amber-600 text-white rounded-lg text-sm font-medium hover:bg-amber-700 disabled:opacity-50"
          >
            {storyLoading ? 'Generating…' : '📖 Story Mode'}
          </button>
        </div>
      </div>

      {loading ? (
        <p className="text-gray-400">Loading cockpit…</p>
      ) : (
        <>
          {/* Metrics Grid */}
          <section className="mb-8" data-testid="cfo-metrics-section">
            <h2 className="text-lg font-semibold mb-3">Key Metrics</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
              {metrics.map(m => (
                <div
                  key={m.metric_id}
                  data-testid="cfo-metric-card"
                  className={`rounded-xl border-2 p-4 ${healthColor(m.health)}`}
                >
                  <div className="text-xs font-medium text-gray-600 mb-1">{m.label}</div>
                  <div className="text-xl font-bold">
                    {typeof m.value === 'number' ? m.value.toLocaleString() : m.value}
                    {m.unit && <span className="text-sm font-normal ml-1">{m.unit}</span>}
                  </div>
                  {m.trend && (
                    <div className="text-xs mt-1 opacity-75">{trendIcon(m.trend)}</div>
                  )}
                </div>
              ))}
              {metrics.length === 0 && (
                <p className="col-span-full text-gray-400">No metrics. Run demo seed.</p>
              )}
            </div>
          </section>

          {/* Scenario Packs */}
          <section className="mb-8" data-testid="cfo-scenarios-section">
            <h2 className="text-lg font-semibold mb-3">Scenario Packs</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {scenarios.map(s => (
                <div
                  key={s.scenario_id}
                  data-testid="cfo-scenario-card"
                  className="rounded-xl border bg-white shadow-sm p-4"
                >
                  <div className="font-semibold text-gray-800">{s.name}</div>
                  {s.description && (
                    <p className="text-sm text-gray-500 mt-1">{s.description}</p>
                  )}
                  <div className="mt-3 space-y-1">
                    {Object.entries(s.metrics || {}).slice(0, 4).map(([k, v]) => (
                      <div key={k} className="flex justify-between text-xs">
                        <span className="text-gray-600">{k}</span>
                        <span className="font-mono font-medium">{typeof v === 'number' ? v.toLocaleString() : v}</span>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
              {scenarios.length === 0 && (
                <p className="col-span-full text-gray-400">No scenario packs.</p>
              )}
            </div>
          </section>

          {/* Story Mode Output */}
          {story && (
            <section className="mb-8" data-testid="cfo-story-section">
              <h2 className="text-lg font-semibold mb-3">Story Mode Narrative</h2>
              <div className="rounded-xl border bg-amber-50 border-amber-200 p-5">
                <p className="text-gray-800 whitespace-pre-wrap">{story.narrative}</p>
                {story.highlights && story.highlights.length > 0 && (
                  <ul className="mt-4 list-disc list-inside text-sm text-gray-700">
                    {story.highlights.map((h, i) => (
                      <li key={i}>{h}</li>
                    ))}
                  </ul>
                )}
              </div>
            </section>
          )}
        </>
      )}
    </div>
  )
}
