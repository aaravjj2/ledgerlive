/**
 * Hackathon Showcase — Single landing page for judges
 * Links to all hackathon-specific features with clear value props.
 * Gemini Live | DigitalOcean Gradient | Airia AI Agents
 */
import { Link } from 'react-router-dom'
import CountdownTimer from '../components/CountdownTimer'
import JudgeScorecard from '../components/JudgeScorecard'
import DemoScript from '../components/DemoScript'

const TRACKS = [
  {
    id: 'gemini-live',
    name: 'Gemini Live Agent Challenge',
    prize: '$80,000',
    deadline: 'Mar 16, 2026',
    features: [
      { path: '/live-voice', label: 'Live Voice CFO', desc: 'Real-time audio I/O, interruptible. Talk to your close assistant.', track: 'Live Agents 🗣️' },
      { path: '/storyteller', label: 'Multimodal Storyteller', desc: 'Interleaved text, images, charts. Close narrative as creative director.', track: 'Creative Storyteller ✍️' },
      { path: '/ui-navigator', label: 'UI Navigator', desc: 'Screenshot-based close flow automation. Agent as your hands on screen.', track: 'UI Navigator ☸️' },
    ],
    color: 'from-blue-600 to-indigo-700',
    badge: 'Google Cloud',
  },
  {
    id: 'digitalocean',
    name: 'DigitalOcean Gradient™ AI Hackathon',
    prize: '$20,000',
    deadline: 'Mar 18, 2026',
    features: [
      { path: '/gradient-ai', label: 'Gradient AI Dashboard', desc: 'Model training, inference, deployment. Full-stack AI lifecycle.', track: 'Full-Stack AI' },
      { path: '/ml-dataset', label: 'ML Dataset Builder', desc: 'Build and manage ML datasets for close intelligence.', track: 'Gradient AI' },
      { path: '/ml-inference', label: 'ML Inference', desc: 'Run inference on exception classification, variance prediction.', track: 'GPU-Powered' },
    ],
    color: 'from-cyan-600 to-blue-600',
    badge: 'DigitalOcean',
  },
  {
    id: 'airia',
    name: 'Airia AI Agents Hackathon',
    prize: '$7,000',
    deadline: 'Mar 19, 2026',
    features: [
      { path: '/airia-everywhere', label: 'Airia Everywhere', desc: 'Browser extension, Slack, Teams, Outlook. Meet users where they are.', track: 'Airia Everywhere 🌐' },
      { path: '/multi-agent', label: 'Multi-Agent Orchestrator', desc: 'Autonomous workflows across 2+ systems. HITL, document generation.', track: 'Active Agents 🤝' },
      { path: '/airia', label: 'Airia Readiness', desc: 'Community bundle, MCP gateway, no-code builder.', track: 'Community Publish' },
    ],
    color: 'from-emerald-600 to-teal-600',
    badge: 'Airia',
  },
]

export default function HackathonShowcase() {
  return (
    <div data-testid="hackathon-showcase-page" className="min-h-screen bg-gray-950 text-white">
      <div className="max-w-6xl mx-auto px-6 py-12">
        <header className="text-center mb-16">
          <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-amber-400 to-orange-500 bg-clip-text text-transparent">
            LedgerLive — Hackathon Showcase
          </h1>
          <p className="text-gray-400 text-lg">
            Finance close agent built for Gemini Live, DigitalOcean Gradient, and Airia AI
          </p>
          <div className="flex justify-center gap-4 mt-6 items-center">
            <CountdownTimer targetDate="2026-03-16T23:59:59Z" label="Gemini Live" compact dataTestId="showcase-countdown" />
            <Link
              to="/race-control"
              className="px-6 py-3 bg-amber-600 hover:bg-amber-500 rounded-lg font-semibold transition"
              data-testid="showcase-race-control"
            >
              ▶ Run Demo
            </Link>
            <Link
              to="/cfo-cockpit"
              className="px-6 py-3 border border-amber-500 text-amber-400 hover:bg-amber-500/10 rounded-lg font-semibold transition"
              data-testid="showcase-cfo"
            >
              CFO Cockpit
            </Link>
          </div>
        </header>

        <div className="grid lg:grid-cols-3 gap-8 mb-12">
          <div className="lg:col-span-2">
            <DemoScript dataTestId="showcase-demo-script" />
          </div>
          <div className="space-y-4">
            <JudgeScorecard trackId="gemini" dataTestId="showcase-judge-gemini" />
            <JudgeScorecard trackId="digitalocean" compact dataTestId="showcase-judge-do" />
            <JudgeScorecard trackId="airia" compact dataTestId="showcase-judge-airia" />
          </div>
        </div>

        <div className="space-y-12">
          {TRACKS.map(track => (
            <section
              key={track.id}
              data-testid={`showcase-track-${track.id}`}
              className={`rounded-2xl bg-gradient-to-br ${track.color} p-8 shadow-2xl`}
            >
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold">{track.name}</h2>
                <div className="flex items-center gap-3">
                  <span className="px-3 py-1 bg-white/20 rounded-full text-sm font-medium">{track.badge}</span>
                  <span className="text-white/80 text-sm">Prize: {track.prize} · Deadline: {track.deadline}</span>
                </div>
              </div>
              <div className="grid md:grid-cols-3 gap-4">
                {track.features.map(f => (
                  <Link
                    key={f.path}
                    to={f.path}
                    data-testid={`showcase-feature-${f.path.replace('/', '')}`}
                    className="block p-4 bg-white/10 hover:bg-white/20 rounded-xl transition backdrop-blur"
                  >
                    <span className="text-amber-200 text-xs font-medium">{f.track}</span>
                    <h3 className="font-semibold mt-1">{f.label}</h3>
                    <p className="text-sm text-white/80 mt-1">{f.desc}</p>
                    <span className="text-amber-300 text-xs mt-2 inline-block">→ Open</span>
                  </Link>
                ))}
              </div>
            </section>
          ))}
        </div>

        <footer className="mt-16 text-center text-gray-500 text-sm">
          <p>LedgerLive — 340 waves · 2040+ routes · Deterministic close orchestration</p>
          <p className="mt-1">#GeminiLiveAgentChallenge #DigitalOceanGradient #AiriaAI</p>
        </footer>
      </div>
    </div>
  )
}
