import { ReactNode } from 'react'

interface ChartCardProps {
  title: string
  children?: ReactNode
  data?: Record<string, number>
  className?: string
  dataTestId?: string
}

function ChartCardInner({ title, children, data, className = '', dataTestId }: ChartCardProps) {
  return (
    <div
      data-testid={dataTestId}
      className={`rounded-xl border bg-white shadow-sm p-4 ${className}`}
    >
      <h3 className="text-sm font-semibold text-gray-700 mb-3">{title}</h3>
      <div className="min-h-[120px]">
        {data && (
          <div className="grid grid-cols-2 gap-4">
            {Object.entries(data).map(([k, v]) => (
              <div key={k}>
                <span className="text-xs text-gray-500 capitalize">{k}</span>
                <div className="text-xl font-bold text-indigo-600">{v}</div>
              </div>
            ))}
          </div>
        )}
        {children}
      </div>
    </div>
  )
}

export { ChartCardInner as ChartCard }
export default ChartCardInner
