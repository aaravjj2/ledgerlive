/**
 * VoiceVisualizer — Real-time audio level bars for Live Voice Agent.
 * Enhances multimodal UX for Gemini Live Agent Challenge.
 */
import { useEffect, useRef, useState } from 'react'

interface VoiceVisualizerProps {
  active?: boolean
  level?: number
  barCount?: number
  className?: string
  dataTestId?: string
}

export function VoiceVisualizer({
  active = false,
  level = 0,
  barCount = 12,
  className = '',
  dataTestId,
}: VoiceVisualizerProps) {
  const [levels, setLevels] = useState<number[]>(Array(barCount).fill(0))
  const rafRef = useRef<number>()

  useEffect(() => {
    if (!active) {
      setLevels(Array(barCount).fill(0))
      return
    }
    const animate = () => {
      setLevels((prev) =>
        prev.map(() => Math.random() * (level || 0.5) + (level || 0.2) * 0.5)
      )
      rafRef.current = requestAnimationFrame(animate)
    }
    rafRef.current = requestAnimationFrame(animate)
    return () => {
      if (rafRef.current) cancelAnimationFrame(rafRef.current)
    }
  }, [active, level, barCount])

  return (
    <div
      data-testid={dataTestId ?? 'voice-visualizer'}
      className={`flex items-end justify-center gap-1 h-12 ${className}`}
    >
      {levels.map((l, i) => (
        <div
          key={i}
          data-testid={`voice-bar-${i}`}
          className="w-1 bg-indigo-500 rounded-full transition-all duration-75"
          style={{ height: `${Math.max(4, l * 100)}%` }}
        />
      ))}
    </div>
  )
}
