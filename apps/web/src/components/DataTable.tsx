import { ReactNode } from 'react'

export interface Column<T> {
  key: string
  header?: string
  label?: string
  /** Accepts cell value or full row; (v: any) allows (v: string) from generated pages */
  render?: ((row: T) => ReactNode) | ((value: unknown) => ReactNode) | ((value: any) => ReactNode)
  className?: string
}

/** Columns use (value: any) so T is inferred from data only; (v: string) from generated pages is accepted */
interface DataTableProps<T = Record<string, unknown>> {
  columns: Array<{ key: string; header?: string; label?: string; render?: (value: any) => ReactNode; className?: string }>
  data: T[]
  keyExtractor?: (row: T) => string
  emptyMessage?: string
  dataTestId?: string
  loading?: boolean
}

function DataTableInner<T>({
  columns,
  data,
  keyExtractor = (row) => String((row as Record<string, unknown>).id ?? (row as Record<string, unknown>).period_id ?? ''),
  emptyMessage = 'No data',
  dataTestId = 'data-table',
  loading = false,
}: DataTableProps<T>) {
  const getHeader = (c: Column<T>) => c.header ?? c.label ?? c.key

  return (
    <div className="rounded-xl border border-[#2A2A3A] bg-[#111118] overflow-hidden" data-testid={dataTestId}>
      <table className="w-full text-sm">
        <thead className="bg-[#1A1A24] border-b border-[#2A2A3A]">
          <tr>
            {columns.map((c) => (
              <th key={c.key} className={`text-left px-4 py-3 font-semibold text-gray-400 uppercase tracking-wide text-xs ${c.className ?? ''}`}>
                {getHeader(c)}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {loading && (
            <tr>
              <td colSpan={columns.length} className="text-center py-8 text-gray-400">
                Loading…
              </td>
            </tr>
          )}
          {!loading && data.length === 0 && (
            <tr>
              <td colSpan={columns.length} className="text-center py-8 text-gray-400">
                {emptyMessage}
              </td>
            </tr>
          )}
          {!loading && data.map((row, idx) => (
            <tr key={keyExtractor(row) || String(idx)} className="border-b border-[#2A2A3A] hover:bg-[#1A1A24] transition-colors">
              {columns.map((col) => {
                const val = (row as Record<string, unknown>)[col.key]
                return (
                  <td key={col.key} className={`px-4 py-3 ${col.className ?? ''}`}>
                    {col.render
                      ? (col.render as (v: unknown) => ReactNode)(val) ?? (col.render as (r: T) => ReactNode)(row)
                      : String(val ?? '—')}
                  </td>
                )
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export { DataTableInner as DataTable }
export default DataTableInner
