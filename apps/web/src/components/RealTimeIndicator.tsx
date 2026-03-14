/**
 * RealTimeIndicator — Shows live/streaming status for voice, inference, etc.
 * Used in Live Voice Agent, Gradient AI, Multi-Agent.
 */
import { useEffect, useState } from 'react'

interface RealTimeIndicatorProps {
  active?: boolean
  label?: string
  pulse?: boolean
  dataTestId?: string
}

export function RealTimeIndicator({
  active = false,
  label = 'Live',
  pulse = true,
  dataTestId = 'realtime-indicator',
}: RealTimeIndicatorProps) {
  const [dot, setDot] = useState(0)

  useEffect(() => {
    if (!active || !pulse) return
    const id = setInterval(() => setDot(d => (d + 1) % 3), 400)
    return () => clearInterval(id)
  }, [active, pulse])

  if (!active) return null

  return (
    <div data-testid={dataTestId} className="inline-flex items-center gap-1.5 text-red-500 text-xs font-medium">
      <span className="relative flex h-2 w-2">
        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75" />
        <span className="relative inline-flex rounded-full h-2 w-2 bg-red-500" />
      </span>
      <span>{label}{'.'.repeat(dot)}</span>
    </div>
  )
}

export default RealTimeIndicator
