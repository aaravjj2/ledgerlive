/**
 * HITLGate — Human-in-the-loop approval gate for Active Agents (Airia track).
 * Shows pending approval with approve/reject and reason.
 */
import { useState } from 'react'

interface HITLGateProps {
  gateId: string
  title: string
  description?: string
  onApprove?: (reason?: string) => void
  onReject?: (reason?: string) => void
  status?: 'pending' | 'approved' | 'rejected'
  className?: string
  dataTestId?: string
}

export function HITLGate({
  gateId,
  title,
  description,
  onApprove,
  onReject,
  status = 'pending',
  className = '',
  dataTestId = 'hitl-gate',
}: HITLGateProps) {
  const [reason, setReason] = useState('')
  const [loading, setLoading] = useState(false)

  const handleApprove = async () => {
    setLoading(true)
    try {
      await onApprove?.(reason || undefined)
    } finally {
      setLoading(false)
    }
  }

  const handleReject = async () => {
    setLoading(true)
    try {
      await onReject?.(reason || undefined)
    } finally {
      setLoading(false)
    }
  }

  const statusColor =
    status === 'approved' ? 'border-green-500 bg-green-500/10' :
    status === 'rejected' ? 'border-red-500 bg-red-500/10' :
    'border-amber-500 bg-amber-500/10'

  return (
    <div
      data-testid={dataTestId}
      className={`rounded-lg border-2 p-4 ${statusColor} ${className}`}
    >
      <div className="flex items-center justify-between mb-2">
        <div>
          <h3 className="font-semibold text-white">{title}</h3>
          {description && <p className="text-sm text-gray-400 mt-0.5">{description}</p>}
        </div>
        <span
          data-testid={`${dataTestId}-status`}
          className={`px-2 py-0.5 rounded text-xs font-bold ${
            status === 'approved' ? 'bg-green-600 text-white' :
            status === 'rejected' ? 'bg-red-600 text-white' :
            'bg-amber-600 text-gray-100'
          }`}
        >
          {status.toUpperCase()}
        </span>
      </div>
      {status === 'pending' && (
        <>
          <textarea
            data-testid={`${dataTestId}-reason`}
            value={reason}
            onChange={(e) => setReason(e.target.value)}
            placeholder="Optional: Add approval/rejection reason…"
            className="w-full mt-2 px-3 py-2 rounded bg-gray-800 text-gray-200 text-sm border border-gray-600 resize-none"
            rows={2}
          />
          <div className="flex gap-2 mt-3">
            <button
              data-testid={`${dataTestId}-approve`}
              onClick={handleApprove}
              disabled={loading}
              className="px-4 py-2 bg-green-600 text-white rounded font-medium hover:bg-green-700 disabled:opacity-50"
            >
              ✓ Approve
            </button>
            <button
              data-testid={`${dataTestId}-reject`}
              onClick={handleReject}
              disabled={loading}
              className="px-4 py-2 bg-red-600 text-white rounded font-medium hover:bg-red-700 disabled:opacity-50"
            >
              ✗ Reject
            </button>
          </div>
        </>
      )}
    </div>
  )
}

export default HITLGate
