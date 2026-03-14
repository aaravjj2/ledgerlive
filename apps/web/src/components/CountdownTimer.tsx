/**
 * CountdownTimer — SLA countdown, deadline display.
 * Used in Race Control, Close Calendar, Bloomberg Terminal.
 */
import { useState, useEffect } from 'react'

interface CountdownTimerProps {
  targetDate: Date | string
  onExpire?: () => void
  label?: string
  compact?: boolean
  dataTestId?: string
}

function pad(n: number) {
  return n.toString().padStart(2, '0')
}

export function CountdownTimer({
  targetDate,
  onExpire,
  label = 'Time remaining',
  compact = false,
  dataTestId = 'countdown-timer',
}: CountdownTimerProps) {
  const target = typeof targetDate === 'string' ? new Date(targetDate) : targetDate
  const [remaining, setRemaining] = useState<{ h: number; m: number; s: number } | null>(null)
  const [expired, setExpired] = useState(false)

  useEffect(() => {
    const tick = () => {
      const now = new Date().getTime()
      const end = target.getTime()
      const diff = end - now

      if (diff <= 0) {
        setExpired(true)
        setRemaining({ h: 0, m: 0, s: 0 })
        onExpire?.()
        return
      }

      const h = Math.floor(diff / (1000 * 60 * 60))
      const m = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
      const s = Math.floor((diff % (1000 * 60)) / 1000)
      setRemaining({ h, m, s })
    }

    tick()
    const id = setInterval(tick, 1000)
    return () => clearInterval(id)
  }, [target, onExpire])

  if (remaining === null) return null

  const str = expired
    ? 'Expired'
    : `${pad(remaining.h)}:${pad(remaining.m)}:${pad(remaining.s)}`

  return (
    <div data-testid={dataTestId} className={compact ? 'text-xs font-mono' : ''}>
      {label && <span className="text-gray-500 mr-1">{label}:</span>}
      <span
        className={
          expired
            ? 'text-red-600 font-semibold'
            : remaining.h < 1
            ? 'text-amber-600 font-semibold'
            : 'text-green-600 font-mono'
        }
      >
        {str}
      </span>
    </div>
  )
}

export default CountdownTimer
