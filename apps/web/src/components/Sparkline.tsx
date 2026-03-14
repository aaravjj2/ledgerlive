/**
 * Sparkline — Mini inline chart for tickers, metrics, trends.
 * Used in TickerBar, Watchlist, Bloomberg Terminal.
 */
import { useMemo } from 'react'
import { LineChart, Line, ResponsiveContainer } from 'recharts'

interface SparklineProps {
  data: number[]
  width?: number
  height?: number
  color?: string
  strokeWidth?: number
  showArea?: boolean
  dataTestId?: string
}

export function Sparkline({
  data,
  width = 80,
  height = 24,
  color = '#10b981',
  strokeWidth = 1.5,
  showArea = false,
  dataTestId = 'sparkline',
}: SparklineProps) {
  const chartData = useMemo(
    () => data.map((v, i) => ({ i, value: v })),
    [data]
  )

  if (!chartData.length) return null

  return (
    <div data-testid={dataTestId} style={{ width, height }} className="inline-block">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={chartData} margin={{ top: 2, right: 2, bottom: 2, left: 2 }}>
          <Line
            type="monotone"
            dataKey="value"
            stroke={color}
            strokeWidth={strokeWidth}
            dot={false}
            fill={showArea ? color : undefined}
            fillOpacity={showArea ? 0.2 : 0}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}

export default Sparkline
