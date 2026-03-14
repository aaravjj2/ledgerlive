/**
 * DemoScript — Step-by-step demo flow for judges.
 * Ensures consistent, winning demo presentation.
 */
import { useState } from 'react'
import { Link } from 'react-router-dom'

export interface DemoStep {
  label: string
  path?: string
  action?: string
  duration?: string
}

const DEFAULT_STEPS: DemoStep[] = [
  { label: 'Open Hackathon Showcase', path: '/showcase', duration: '30s' },
  { label: 'Run Race Control demo', path: '/race-control', action: 'Click ▶ Run', duration: '2m' },
  { label: 'Live Voice CFO', path: '/live-voice', action: 'Click mic, speak', duration: '1m' },
  { label: 'Multimodal Storyteller', path: '/storyteller', action: 'Upload doc, generate', duration: '1m' },
  { label: 'UI Navigator', path: '/ui-navigator', action: 'Capture screen, instruct', duration: '1m' },
  { label: 'Gradient AI Dashboard', path: '/gradient-ai', action: 'Show training/inference', duration: '1m' },
  { label: 'Airia Everywhere', path: '/airia-everywhere', action: 'Show integrations', duration: '45s' },
  { label: 'Multi-Agent Orchestrator', path: '/multi-agent', action: 'Trigger workflow, HITL', duration: '1m' },
]

interface DemoScriptProps {
  steps?: DemoStep[]
  title?: string
  dataTestId?: string
}

export function DemoScript({ steps = DEFAULT_STEPS, title = 'Judge demo script', dataTestId = 'demo-script' }: DemoScriptProps) {
  const [current, setCurrent] = useState(0)

  return (
    <div data-testid={dataTestId} className="rounded-xl border border-amber-500/30 bg-amber-950/20 p-4">
      <h3 className="font-semibold text-amber-200 mb-3">{title}</h3>
      <ol className="space-y-2">
        {steps.map((s, i) => (
          <li key={i} className="flex items-center gap-3">
            <button
              onClick={() => setCurrent(i)}
              className={`w-7 h-7 rounded-full flex items-center justify-center text-sm font-medium transition ${
                current === i ? 'bg-amber-500 text-black' : 'bg-gray-700 text-gray-400 hover:bg-gray-600'
              }`}
            >
              {i + 1}
            </button>
            <div className="flex-1">
              <span className={current === i ? 'text-amber-100 font-medium' : 'text-gray-400'}>{s.label}</span>
              {s.path && (
                <Link to={s.path} className="ml-2 text-amber-400 hover:underline text-sm">
                  {s.path}
                </Link>
              )}
              {s.action && <span className="ml-2 text-gray-500 text-sm">— {s.action}</span>}
              {s.duration && <span className="ml-2 text-gray-600 text-xs">({s.duration})</span>}
            </div>
          </li>
        ))}
      </ol>
    </div>
  )
}

export default DemoScript
