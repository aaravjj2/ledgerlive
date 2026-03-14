/**
 * hackathonTracks — Central config for all 3 hackathons.
 * Used by HackathonShowcase, JudgeScorecard, DemoScript.
 */

export interface HackathonTrack {
  id: string
  name: string
  prize: string
  deadline: string
  url?: string
  features: { path: string; label: string; desc: string; track: string }[]
  color: string
  badge: string
}

export const HACKATHON_TRACKS: HackathonTrack[] = [
  {
    id: 'gemini-live',
    name: 'Gemini Live Agent Challenge',
    prize: '$80,000',
    deadline: '2026-03-16',
    url: 'https://geminiliveagentchallenge.devpost.com/',
    features: [
      { path: '/live-voice', label: 'Live Voice CFO', desc: 'Real-time audio I/O, interruptible.', track: 'Live Agents' },
      { path: '/storyteller', label: 'Multimodal Storyteller', desc: 'Interleaved text, images, charts.', track: 'Creative Storyteller' },
      { path: '/ui-navigator', label: 'UI Navigator', desc: 'Screenshot-based automation.', track: 'UI Navigator' },
    ],
    color: 'from-blue-600 to-indigo-700',
    badge: 'Google Cloud',
  },
  {
    id: 'digitalocean',
    name: 'DigitalOcean Gradient™ AI Hackathon',
    prize: '$20,000',
    deadline: '2026-03-18',
    url: 'https://digitalocean.devpost.com/',
    features: [
      { path: '/gradient-ai', label: 'Gradient AI Dashboard', desc: 'Training, inference, deployment.', track: 'Full-Stack AI' },
      { path: '/ml-dataset', label: 'ML Dataset Builder', desc: 'Build ML datasets.', track: 'Gradient AI' },
      { path: '/ml-inference', label: 'ML Inference', desc: 'Exception classification, variance prediction.', track: 'GPU-Powered' },
    ],
    color: 'from-cyan-600 to-blue-600',
    badge: 'DigitalOcean',
  },
  {
    id: 'airia',
    name: 'Airia AI Agents Hackathon',
    prize: '$7,000',
    deadline: '2026-03-19',
    url: 'https://airia-hackathon.devpost.com/',
    features: [
      { path: '/airia-everywhere', label: 'Airia Everywhere', desc: 'Browser, Slack, Teams, Outlook.', track: 'Airia Everywhere' },
      { path: '/multi-agent', label: 'Multi-Agent Orchestrator', desc: 'HITL, document generation.', track: 'Active Agents' },
      { path: '/airia', label: 'Airia Readiness', desc: 'Community bundle, MCP gateway.', track: 'Community Publish' },
    ],
    color: 'from-emerald-600 to-teal-600',
    badge: 'Airia',
  },
]
