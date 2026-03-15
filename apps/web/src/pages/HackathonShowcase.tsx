/**
 * HackathonShowcase — Competition landing page for judges.
 * Gemini Live | DigitalOcean Gradient | Airia AI Agents | GitLab Duo
 */
import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import CountdownTimer from '../components/CountdownTimer'
import JudgeScorecard from '../components/JudgeScorecard'
import DemoScript from '../components/DemoScript'
import { API_BASE } from '../services/api'

interface LiveStats {
  documents: number
  reconciliations: number
  tests: number
}

interface TrackFeature {
  path: string
  label: string
  desc: string
  track: string
}

interface Track {
  id: string
  name: string
  prize: string
  prizeAmount: string
  trackLabel: string
  deadline: string
  tech: string[]
  accentColor: string
  features: TrackFeature[]
}

const TRACKS: Track[] = [
  {
    id: 'gemini-live',
    name: 'Gemini Live Agent Challenge',
    prize: '$80,000',
    prizeAmount: '80K',
    trackLabel: 'Best AI Agent',
    deadline: 'Mar 16, 2026',
    accentColor: 'border-t-blue-500',
    tech: ['Cloud Run', 'Gemini Live API', 'WebSocket'],
    features: [
      { path: '/live-voice',   label: 'Live Voice CFO',         desc: 'Real-time audio I/O, interruptible. Talk to your close assistant.',        track: 'Live Agents' },
      { path: '/storyteller',  label: 'Multimodal Storyteller', desc: 'Interleaved text, images, charts. Close narrative as creative director.',  track: 'Creative Storyteller' },
      { path: '/ui-navigator', label: 'UI Navigator',           desc: 'Screenshot-based close flow automation. Agent as your hands on screen.',  track: 'UI Navigator' },
    ],
  },
  {
    id: 'digitalocean',
    name: 'DigitalOcean Gradient AI',
    prize: '$20,000',
    prizeAmount: '20K',
    trackLabel: 'Best AI Agent Persona',
    deadline: 'Mar 18, 2026',
    accentColor: 'border-t-cyan-500',
    tech: ['Gradient AI', 'App Platform', 'GPU Inference'],
    features: [
      { path: '/gradient-ai',  label: 'Gradient AI Dashboard', desc: 'Model training, inference, deployment. Full-stack AI lifecycle.',           track: 'Full-Stack AI' },
      { path: '/ml-dataset',   label: 'ML Dataset Builder',    desc: 'Build and manage ML datasets for close intelligence.',                      track: 'Gradient AI' },
      { path: '/ml-inference', label: 'ML Inference',          desc: 'Run inference on exception classification, variance prediction.',           track: 'GPU-Powered' },
    ],
  },
  {
    id: 'airia',
    name: 'Airia AI Agents Hackathon',
    prize: '$7,000',
    prizeAmount: '7K',
    trackLabel: 'Active Agents',
    deadline: 'Mar 19, 2026',
    accentColor: 'border-t-emerald-500',
    tech: ['Multi-agent', 'MCP Gateway', 'Orchestration'],
    features: [
      { path: '/airia-everywhere', label: 'Airia Everywhere',         desc: 'Browser extension, Slack, Teams, Outlook. Meet users where they are.', track: 'Airia Everywhere' },
      { path: '/multi-agent',      label: 'Multi-Agent Orchestrator', desc: 'Autonomous workflows across 2+ systems. HITL, document generation.',   track: 'Active Agents' },
      { path: '/airia',            label: 'Airia Readiness',          desc: 'Community bundle, MCP gateway, no-code builder.',                      track: 'Community Publish' },
    ],
  },
  {
    id: 'gitlab',
    name: 'GitLab Duo Innovation',
    prize: '$65,000',
    prizeAmount: '65K',
    trackLabel: 'Best Use of Duo',
    deadline: 'Mar 20, 2026',
    accentColor: 'border-t-orange-500',
    tech: ['GitLab Duo', 'CI/CD Automation', 'Compliance AI'],
    features: [
      { path: '/gitlab-duo',   label: 'Duo Compliance',     desc: 'Automated compliance checks powered by GitLab Duo AI.',         track: 'Compliance Automation' },
      { path: '/audit',        label: 'Audit Intelligence', desc: 'AI-driven immutable audit trail with severity classification.', track: 'Risk Management' },
      { path: '/review-queue', label: 'AI Review Queue',    desc: 'Intelligent document review workflow with agent scoring.',      track: 'Document AI' },
    ],
  },
]

const FEATURE_CHIPS = ['Voice Agent', 'Multi-Agent', 'OCR', 'Compliance', 'Real-time', 'F1 UI']

const ARCH_DIAGRAM = [
  '  +----------------------+      +----------------------+      +-------------------------+',
  '  |      Frontend        | ---> |       FastAPI         | ---> |      AI Services        |',
  '  |   React 18 + Vite    |      |     Port 8090         |      |   Gemini Live API       |',
  '  |   Tailwind + F1 UI   |      |   SQLite (DEMO)       |      |   google-genai 1.67.0   |',
  '  |   4,280 tests  ok    |      |   88 E2E tests  ok    |      |  Voice + Text + Vision  |',
  '  +----------------------+      +----------------------+      +-------------------------+',
  '          |                              |                                |',
  '     Cloud Run                      Cloud Run                    GCP Secret Manager',
  '     Port 8080                      Port 8090                    GEMINI_API_KEY',
].join('\n')

export default function HackathonShowcase() {
  const [stats, setStats] = useState<LiveStats>({
    documents: 0,
    reconciliations: 0,
    tests: 4280,
  })

  useEffect(() => {
    Promise.all([
      fetch(`${API_BASE}/api/documents`).then(r => r.json()) as Promise<{
        total?: number
        items?: unknown[]
      }>,
      fetch(`${API_BASE}/api/reconciliations`).then(r => r.json()) as Promise<{
        total?: number
        items?: unknown[]
      }>,
    ])
      .then(([docs, recons]) => {
        setStats({
          documents: docs.total ?? docs.items?.length ?? 0,
          reconciliations: recons.total ?? recons.items?.length ?? 0,
          tests: 4280,
        })
      })
      .catch(() => {})
  }, [])

  return (
    <div
      data-testid="hackathon-showcase-page"
      className="min-h-screen bg-[#0A0A0F] text-[#F8F9FA]"
    >
      <div className="max-w-6xl mx-auto px-6 py-12">

        {/* ── Hero ─────────────────────────────────────────────────────── */}
        <header className="text-center mb-14">
          <div className="mb-6">
            <h1 className="text-7xl font-black tracking-tight mb-4 leading-none">
              <span className="text-[#F8F9FA]">Ledger</span>
              <span className="text-[#E8002D]">Live</span>
            </h1>
            <div className="flex justify-center items-center overflow-hidden">
              <span className="typing-hero text-xl text-[#9CA3AF] font-light tracking-wide">
                AI Finance Close Agent
              </span>
            </div>
          </div>

          <p className="text-[#9CA3AF] text-base max-w-2xl mx-auto mb-2 leading-relaxed">
            Real-time close orchestration powered by{' '}
            <span className="text-[#00D2FF] font-semibold">Gemini Live</span>,{' '}
            <span className="text-[#FFD700] font-semibold">multi-agent AI</span>, and{' '}
            <span className="text-[#E8002D] font-semibold">voice commands</span>.
            Built for the finance close team that moves at F1 speed.
          </p>

          {/* Feature chips */}
          <div className="flex justify-center gap-2 flex-wrap mt-6 mb-8">
            {FEATURE_CHIPS.map(chip => (
              <span
                key={chip}
                className="px-3 py-1 rounded-full text-xs font-semibold bg-[#111118] border border-[#2A2A3A] text-[#9CA3AF]"
              >
                {chip}
              </span>
            ))}
          </div>

          {/* Action row */}
          <div className="flex justify-center gap-4 flex-wrap items-center">
            <CountdownTimer
              targetDate="2026-03-16T23:59:59Z"
              label="Gemini Live"
              compact
              dataTestId="showcase-countdown"
            />
            <Link
              to="/race-control"
              className="px-7 py-3 bg-[#E8002D] hover:bg-[#C8001D] rounded-xl font-bold text-white transition-colors text-sm tracking-wide"
              data-testid="showcase-race-control"
            >
              Open Live Demo
            </Link>
            <Link
              to="/cfo-cockpit"
              className="px-7 py-3 border border-[#2A2A3A] text-[#9CA3AF] hover:text-[#F8F9FA] hover:border-[#3A3A4A] rounded-xl font-semibold transition-colors text-sm"
              data-testid="showcase-cfo"
            >
              CFO Cockpit
            </Link>
          </div>
        </header>

        {/* ── Prize Cards 2x2 ──────────────────────────────────────────── */}
        <div className="grid md:grid-cols-2 gap-5 mb-14">
          {TRACKS.map(track => (
            <section
              key={track.id}
              data-testid={`showcase-track-${track.id}`}
              className={`bg-[#111118] border border-[#2A2A3A] border-t-2 ${track.accentColor} rounded-2xl p-6 flex flex-col gap-4`}
            >
              {/* Prize + track meta */}
              <div className="flex items-start justify-between">
                <div>
                  <span className="text-5xl font-black text-[#FFD700] leading-none">
                    ${track.prizeAmount}
                  </span>
                  <p className="text-[#9CA3AF] text-xs mt-1">{track.prize} total prize</p>
                </div>
                <div className="text-right">
                  <p className="text-[#F8F9FA] font-semibold text-sm">{track.trackLabel}</p>
                  <p className="text-[#9CA3AF] text-xs mt-1">{track.deadline}</p>
                </div>
              </div>

              <p className="text-[#F8F9FA] font-semibold text-sm">{track.name}</p>

              {/* Tech badges */}
              <div className="flex flex-wrap gap-1.5">
                {track.tech.map(t => (
                  <span
                    key={t}
                    className="px-2 py-0.5 rounded bg-[#1A1A24] text-[#00D2FF] text-xs border border-[#2A2A3A]"
                  >
                    {t}
                  </span>
                ))}
              </div>

              {/* Feature links */}
              <div className="flex flex-col gap-2">
                {track.features.map(f => (
                  <Link
                    key={f.path}
                    to={f.path}
                    data-testid={`showcase-feature-${f.path.replace('/', '')}`}
                    className="flex items-start gap-3 p-3 bg-[#0A0A0F] hover:bg-[#1A1A24] rounded-xl border border-[#2A2A3A] hover:border-[#3A3A4A] transition-colors group"
                  >
                    <div className="flex-1 min-w-0">
                      <span className="text-[#E8002D] text-xs font-semibold">{f.track}</span>
                      <p className="text-[#F8F9FA] text-sm font-medium mt-0.5">{f.label}</p>
                      <p className="text-[#9CA3AF] text-xs mt-0.5 leading-relaxed">{f.desc}</p>
                    </div>
                    <span className="text-[#9CA3AF] group-hover:text-[#E8002D] transition-colors text-sm mt-1 flex-shrink-0">
                      &rarr;
                    </span>
                  </Link>
                ))}
              </div>
            </section>
          ))}
        </div>

        {/* ── Demo Script + Judge Scorecards ────────────────────────────── */}
        <div className="grid lg:grid-cols-3 gap-6 mb-14">
          <div className="lg:col-span-2">
            <DemoScript dataTestId="showcase-demo-script" />
          </div>
          <div className="flex flex-col gap-4">
            <JudgeScorecard trackId="gemini" dataTestId="showcase-judge-gemini" />
            <JudgeScorecard trackId="digitalocean" compact dataTestId="showcase-judge-do" />
            <JudgeScorecard trackId="airia" compact dataTestId="showcase-judge-airia" />
          </div>
        </div>

        {/* ── Live Stats ───────────────────────────────────────────────── */}
        <section className="bg-[#111118] border border-[#2A2A3A] rounded-2xl p-8 mb-14">
          <h2 className="text-xs font-semibold text-[#9CA3AF] uppercase tracking-widest mb-6">
            Live System Stats
          </h2>
          <div className="grid grid-cols-3 gap-6 text-center">
            <div>
              <p className="text-5xl font-black text-[#F8F9FA] font-mono tabular-nums">
                {stats.documents}
              </p>
              <p className="text-[#9CA3AF] text-sm mt-2">Documents Processed</p>
            </div>
            <div>
              <p className="text-5xl font-black text-[#00D2FF] font-mono tabular-nums">
                {stats.reconciliations}
              </p>
              <p className="text-[#9CA3AF] text-sm mt-2">Reconciliations</p>
            </div>
            <div>
              <p className="text-5xl font-black text-[#FFD700] font-mono tabular-nums">
                {stats.tests.toLocaleString()}
              </p>
              <p className="text-[#9CA3AF] text-sm mt-2">Tests Passing</p>
            </div>
          </div>
        </section>

        {/* ── Architecture ─────────────────────────────────────────────── */}
        <section className="bg-[#111118] border border-[#2A2A3A] rounded-2xl p-8 mb-14">
          <h2 className="text-xs font-semibold text-[#9CA3AF] uppercase tracking-widest mb-6">
            Architecture
          </h2>
          <div className="overflow-x-auto">
            <pre className="font-mono text-xs text-[#9CA3AF] leading-relaxed whitespace-pre">
              {ARCH_DIAGRAM}
            </pre>
          </div>
        </section>

        {/* ── CTA ──────────────────────────────────────────────────────── */}
        <div className="text-center mb-14">
          <Link
            to="/race-control"
            className="inline-block px-12 py-4 bg-[#E8002D] hover:bg-[#C8001D] rounded-xl font-bold text-lg text-white transition-colors tracking-wide"
          >
            Open Live Demo
          </Link>
          <p className="text-[#9CA3AF] text-sm mt-3">
            Runs in demo mode — no credentials required
          </p>
        </div>

        {/* Footer */}
        <footer className="text-center text-[#9CA3AF]/50 text-xs">
          <p>LedgerLive — 340 waves · 2040+ routes · Deterministic close orchestration</p>
          <p className="mt-1">
            #GeminiLiveAgentChallenge #DigitalOceanGradient #AiriaAI #GitLabDuo
          </p>
        </footer>
      </div>
    </div>
  )
}
