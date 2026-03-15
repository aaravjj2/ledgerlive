import clsx from 'clsx'

interface StatusBadgeProps {
  status: string
  variant?: 'default' | 'severity' | 'health'
  dataTestId?: string
}

const STATUS_COLORS: Record<string, string> = {
  ok: 'bg-green-900/40 text-green-400',
  pass: 'bg-green-900/40 text-green-400',
  approved: 'bg-green-900/40 text-green-400',
  completed: 'bg-green-900/40 text-green-400',
  resolved: 'bg-green-900/40 text-green-400',
  pending: 'bg-yellow-900/40 text-yellow-400',
  open: 'bg-yellow-900/40 text-yellow-400',
  active: 'bg-blue-900/40 text-blue-400',
  error: 'bg-red-900/40 text-red-400',
  failed: 'bg-red-900/40 text-red-400',
  rejected: 'bg-red-900/40 text-red-400',
  critical: 'bg-red-600 text-white',
  high: 'bg-orange-500 text-white',
  medium: 'bg-yellow-400 text-gray-100',
  low: 'bg-[#1A1A24] text-gray-400 border border-[#2A2A3A]',
  green: 'bg-green-900/40 text-green-300',
  yellow: 'bg-yellow-900/40 text-yellow-300',
  red: 'bg-red-900/40 text-red-400',
}

function StatusBadgeInner({ status, variant = 'default', dataTestId }: StatusBadgeProps) {
  const s = (status || 'unknown').toLowerCase()
  const color = STATUS_COLORS[s] ?? 'bg-[#1A1A24] text-gray-400'
  return (
    <span
      data-testid={dataTestId}
      className={clsx('px-2 py-0.5 rounded-full text-xs font-medium', color)}
    >
      {status || '—'}
    </span>
  )
}

export { StatusBadgeInner as StatusBadge }
export default StatusBadgeInner
