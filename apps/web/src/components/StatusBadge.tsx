import clsx from 'clsx'

interface StatusBadgeProps {
  status: string
  variant?: 'default' | 'severity' | 'health'
  dataTestId?: string
}

const STATUS_COLORS: Record<string, string> = {
  ok: 'bg-green-100 text-green-700',
  pass: 'bg-green-100 text-green-700',
  approved: 'bg-green-100 text-green-700',
  completed: 'bg-green-100 text-green-700',
  resolved: 'bg-green-100 text-green-700',
  pending: 'bg-yellow-100 text-yellow-700',
  open: 'bg-yellow-100 text-yellow-700',
  active: 'bg-blue-100 text-blue-700',
  error: 'bg-red-100 text-red-700',
  failed: 'bg-red-100 text-red-700',
  rejected: 'bg-red-100 text-red-700',
  critical: 'bg-red-600 text-white',
  high: 'bg-orange-500 text-white',
  medium: 'bg-yellow-400 text-gray-900',
  low: 'bg-gray-200 text-gray-700',
  green: 'bg-green-100 text-green-800',
  yellow: 'bg-yellow-100 text-yellow-800',
  red: 'bg-red-100 text-red-800',
}

function StatusBadgeInner({ status, variant = 'default', dataTestId }: StatusBadgeProps) {
  const s = (status || 'unknown').toLowerCase()
  const color = STATUS_COLORS[s] ?? 'bg-gray-100 text-gray-600'
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
