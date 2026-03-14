/**
 * JudgeScorecard — Shows hackathon judge criteria alignment.
 * Used on HackathonShowcase to demonstrate how LedgerLive meets each track's requirements.
 */
import { judgeChecklist } from '../utils/judgeChecklist'

interface JudgeScorecardProps {
  trackId: 'gemini' | 'digitalocean' | 'airia'
  compact?: boolean
  dataTestId?: string
}

export function JudgeScorecard({ trackId, compact = false, dataTestId = 'judge-scorecard' }: JudgeScorecardProps) {
  const criteria = judgeChecklist[trackId] ?? []
  const met = criteria.filter(c => c.met).length
  const total = criteria.length
  const pct = total ? Math.round((met / total) * 100) : 0

  return (
    <div data-testid={dataTestId} className={`rounded-xl border border-gray-700 bg-gray-900/50 p-4 ${compact ? 'text-sm' : ''}`}>
      <div className="flex items-center justify-between mb-2">
        <span className="font-medium text-gray-300">Judge criteria</span>
        <span className={`font-mono font-bold ${pct >= 80 ? 'text-green-400' : pct >= 50 ? 'text-amber-400' : 'text-red-400'}`}>
          {met}/{total} ({pct}%)
        </span>
      </div>
      <ul className="space-y-1">
        {criteria.map((c, i) => (
          <li key={i} className="flex items-center gap-2">
            <span>{c.met ? '✓' : '○'}</span>
            <span className={c.met ? 'text-gray-300' : 'text-gray-500'}>{c.label}</span>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default JudgeScorecard
