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

type Period = 'Q1 2026' | 'Q2 2026' | 'Full Year'

const PERIODS: Period[] = ['Q1 2026', 'Q2 2026', 'Full Year']

const SCENARIO_ACCENTS = [
  { bar: 'bg-[#00D2FF]', badge: 'bg-[#00D2FF]/10 text-[#00D2FF]', label: 'S1' },
  { bar: 'bg-[#FFD700]', badge: 'bg-[#FFD700]/10 text-[#FFD700]', label: 'S2' },
  { bar: 'bg-red-400',   badge: 'bg-red-900/30 text-red-400',      label: 'S3' },
]

export default function CFOCockpit() {
  const [metrics, setMetrics] = useState<CockpitMetric[]>([])
  const [scenarios, setScenarios] = useState<ScenarioPack[]>([])
  const [story, setStory] = useState<StoryModeResult | null>(null)
  const [loading, setLoading] = useState(true)
  const [storyLoading, setStoryLoading] = useState(false)
  const [activePeriod, setActivePeriod] = useState<Period>('Q1 2026')
  const [signOffLoading, setSignOffLoading] = useState(false)
  const [signedOff, setSignedOff] = useState(false)

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
    if (h === 'green')  return 'bg-green-900/40 text-green-300 border-green-800'
    if (h === 'yellow') return 'bg-yellow-900/40 text-yellow-300 border-yellow-800'
    if (h === 'red')    return 'bg-red-900/40 text-red-400 border-red-800'
    return 'bg-[#1A1A24] text-gray-200 border-[#2A2A3A]'
  }

  const trendIcon = (t?: string) => {
    if (t === 'up')   return { icon: '▲', color: 'text-green-400' }
    if (t === 'down') return { icon: '▼', color: 'text-red-400' }
    return { icon: '—', color: 'text-gray-500' }
  }

  const healthAccent = (h?: string) => {
    if (h === 'green')  return 'bg-green-400'
    if (h === 'yellow') return 'bg-yellow-400'
    if (h === 'red')    return 'bg-red-400'
    return 'bg-[#00D2FF]'
  }

  const handleSignOff = async () => {
    setSignOffLoading(true)
    try {
      await fetch('/api/cfo/signoff', { method: 'POST' })
      setSignedOff(true)
    } catch {
      // silent
    }
    setSignOffLoading(false)
  }

  return (
    <div data-testid="cfo-cockpit-page" className="min-h-screen bg-[#0A0A0F] pb-16">

      {/* ── Page Header ── */}
      <div className="border-b border-[#2A2A3A] bg-[#111118] px-6 py-5">
        <div className="flex items-start justify-between gap-4 flex-wrap">
          <div>
            <div className="flex items-center gap-3 mb-1">
              <div className="w-1.5 h-8 bg-red-500 rounded-full shrink-0" />
              <h1
                className="text-3xl font-bold tracking-tight text-[#F8F9FA]"
                data-testid="cfo-cockpit-title"
              >
                CFO Cockpit
              </h1>
            </div>
            <p className="text-[#9CA3AF] text-sm ml-5">
              Executive metrics &middot; Scenario packs &middot; Narrative intelligence
            </p>
          </div>

          <div className="flex items-center gap-3 flex-wrap">
            {/* Period selector */}
            <div className="flex rounded-lg overflow-hidden border border-[#2A2A3A]">
              {PERIODS.map(p => (
                <button
                  key={p}
                  onClick={() => setActivePeriod(p)}
                  className={`px-3 py-1.5 text-xs font-semibold transition-colors ${
                    activePeriod === p
                      ? 'bg-red-600 text-white'
                      : 'bg-[#1A1A24] text-[#9CA3AF] hover:text-[#F8F9FA] hover:bg-[#2A2A3A]'
                  }`}
                >
                  {p}
                </button>
              ))}
            </div>

            <button
              data-testid="cfo-cockpit-refresh"
              onClick={loadCockpit}
              className="px-4 py-2 bg-[#1A1A24] border border-[#2A2A3A] text-[#F8F9FA] rounded-lg text-sm font-medium hover:bg-[#2A2A3A] transition-colors"
            >
              &#8635; Refresh
            </button>

            <button
              data-testid="cfo-story-mode"
              onClick={runStoryMode}
              disabled={storyLoading}
              className="px-4 py-2 bg-amber-600 text-white rounded-lg text-sm font-medium hover:bg-amber-500 disabled:opacity-50 transition-colors"
            >
              {storyLoading ? 'Generating\u2026' : '\u25B6 Story Mode'}
            </button>
          </div>
        </div>
      </div>

      <div className="px-6 pt-8 space-y-8">
        {loading ? (
          <div className="flex items-center justify-center py-24">
            <div className="text-center space-y-3">
              <div className="w-8 h-8 border-2 border-red-500 border-t-transparent rounded-full animate-spin mx-auto" />
              <p className="text-[#9CA3AF] text-sm">Loading cockpit data\u2026</p>
            </div>
          </div>
        ) : (
          <>

            {/* ── KPI Hero Row ── */}
            <section data-testid="cfo-metrics-section">
              <div className="flex items-center gap-2 mb-4">
                <span className="text-xs font-semibold text-[#9CA3AF] uppercase tracking-widest">
                  Key Performance Indicators
                </span>
                <div className="flex-1 h-px bg-[#2A2A3A]" />
                <span className="text-xs text-[#9CA3AF] font-mono">{activePeriod}</span>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
                {metrics.map(m => {
                  const trend = trendIcon(m.trend)
                  return (
                    <div
                      key={m.metric_id}
                      data-testid="cfo-metric-card"
                      className={`rounded-xl border p-4 relative overflow-hidden transition-transform hover:-translate-y-0.5 ${healthColor(m.health)}`}
                    >
                      {/* Top accent stripe */}
                      <div className={`absolute top-0 left-0 right-0 h-0.5 ${healthAccent(m.health)}`} />

                      <div className="text-[10px] font-semibold opacity-60 uppercase tracking-wider mb-2">
                        {m.label}
                      </div>

                      <div className="text-2xl font-bold tracking-tight mb-1 leading-none">
                        {typeof m.value === 'number' ? m.value.toLocaleString() : m.value}
                        {m.unit && (
                          <span className="text-xs font-normal ml-1 opacity-70">{m.unit}</span>
                        )}
                      </div>

                      {m.trend && (
                        <div className={`text-xs font-semibold flex items-center gap-1 mt-1 ${trend.color}`}>
                          <span>{trend.icon}</span>
                          <span className="opacity-70 text-[10px]">vs budget</span>
                        </div>
                      )}
                    </div>
                  )
                })}

                {metrics.length === 0 && (
                  <div className="col-span-full py-12 text-center">
                    <p className="text-[#9CA3AF] text-sm">
                      No metrics available. Run demo seed to populate.
                    </p>
                  </div>
                )}
              </div>
            </section>

            {/* ── Scenario Pack Comparison ── */}
            <section data-testid="cfo-scenarios-section">
              <div className="flex items-center gap-2 mb-4">
                <span className="text-xs font-semibold text-[#9CA3AF] uppercase tracking-widest">
                  Scenario Packs
                </span>
                <div className="flex-1 h-px bg-[#2A2A3A]" />
                <span className="text-xs text-[#9CA3AF] font-mono">{scenarios.length} loaded</span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {scenarios.map((s, idx) => {
                  const accent = SCENARIO_ACCENTS[idx % SCENARIO_ACCENTS.length]
                  return (
                    <div
                      key={s.scenario_id}
                      data-testid="cfo-scenario-card"
                      className="rounded-xl border border-[#2A2A3A] bg-[#111118] p-5 relative overflow-hidden hover:border-[#3A3A4A] transition-colors"
                    >
                      {/* Left accent bar */}
                      <div className={`absolute top-0 left-0 bottom-0 w-0.5 ${accent.bar}`} />

                      <div className="pl-3">
                        <div className="flex items-start justify-between mb-2">
                          <div className="font-semibold text-[#F8F9FA] text-sm leading-snug">
                            {s.name}
                          </div>
                          <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ml-2 shrink-0 ${accent.badge}`}>
                            {accent.label}
                          </span>
                        </div>

                        {s.description && (
                          <p className="text-xs text-[#9CA3AF] mb-3 leading-relaxed">
                            {s.description}
                          </p>
                        )}

                        <div className="space-y-1.5">
                          {Object.entries(s.metrics || {}).slice(0, 4).map(([k, v]) => (
                            <div key={k} className="flex justify-between items-center">
                              <span className="text-[11px] text-[#9CA3AF] capitalize">
                                {k.replace(/_/g, ' ')}
                              </span>
                              <span className="font-mono text-xs font-semibold text-[#F8F9FA]">
                                {typeof v === 'number' ? v.toLocaleString() : String(v)}
                              </span>
                            </div>
                          ))}
                        </div>

                        {s.created_at && (
                          <div className="mt-3 pt-3 border-t border-[#2A2A3A]">
                            <span className="text-[10px] text-[#9CA3AF] font-mono">
                              {new Date(s.created_at).toLocaleDateString()}
                            </span>
                          </div>
                        )}
                      </div>
                    </div>
                  )
                })}

                {scenarios.length === 0 && (
                  <div className="col-span-full py-10 text-center">
                    <p className="text-[#9CA3AF] text-sm">No scenario packs loaded.</p>
                  </div>
                )}
              </div>
            </section>

            {/* ── Story Mode Output ── */}
            {story && (
              <section data-testid="cfo-story-section">
                <div className="flex items-center gap-2 mb-4">
                  <span className="text-xs font-semibold text-[#9CA3AF] uppercase tracking-widest">
                    Narrative Story Mode
                  </span>
                  <div className="flex-1 h-px bg-[#2A2A3A]" />
                </div>

                <div className="rounded-xl border border-amber-700/50 bg-amber-950/20 p-6 relative overflow-hidden">
                  {/* Top gradient stripe */}
                  <div className="absolute top-0 left-0 right-0 h-0.5 bg-gradient-to-r from-amber-600 via-amber-400 to-amber-600 rounded-t-xl" />

                  <div className="flex items-center gap-2 mb-4">
                    <div className="w-2 h-2 rounded-full bg-amber-400 animate-pulse" />
                    <span className="text-xs font-semibold text-amber-400 uppercase tracking-widest">
                      AI-Generated Narrative
                    </span>
                  </div>

                  <p className="text-[#F8F9FA] whitespace-pre-wrap leading-relaxed text-sm">
                    {story.narrative}
                  </p>

                  {story.highlights && story.highlights.length > 0 && (
                    <ul className="mt-5 space-y-2">
                      {story.highlights.map((h, i) => (
                        <li key={i} className="flex items-start gap-2 text-sm text-[#F8F9FA]">
                          <span className="text-amber-400 mt-0.5 shrink-0">&#9670;</span>
                          <span>{h}</span>
                        </li>
                      ))}
                    </ul>
                  )}
                </div>
              </section>
            )}

            {/* ── CFO Sign-Off ── */}
            <section>
              <div className="flex items-center gap-2 mb-4">
                <span className="text-xs font-semibold text-[#9CA3AF] uppercase tracking-widest">
                  CFO Sign-Off
                </span>
                <div className="flex-1 h-px bg-[#2A2A3A]" />
              </div>

              <div className="rounded-xl border border-[#2A2A3A] bg-[#111118] p-6">
                <div className="flex items-center justify-between flex-wrap gap-4">
                  <div>
                    <div className="text-[#F8F9FA] font-semibold mb-1">
                      Authorize Period Close
                    </div>
                    <p className="text-[#9CA3AF] text-sm">
                      Digitally approve the {activePeriod} financials and lock the reporting period.
                    </p>
                  </div>

                  <div className="flex items-center gap-3">
                    {signedOff && (
                      <span className="text-xs font-semibold text-green-400 bg-green-900/40 px-3 py-1.5 rounded-full border border-green-800">
                        SIGNED OFF
                      </span>
                    )}
                    <button
                      onClick={handleSignOff}
                      disabled={signOffLoading || signedOff}
                      className="px-6 py-3 bg-red-600 text-white rounded-lg font-semibold text-sm hover:bg-red-500 disabled:opacity-50 transition-colors min-w-[160px] text-center"
                    >
                      {signOffLoading ? 'Processing\u2026' : signedOff ? 'Approved' : 'CFO Sign-Off'}
                    </button>
                  </div>
                </div>
              </div>
            </section>

          </>
        )}
      </div>
    </div>
  )
}
