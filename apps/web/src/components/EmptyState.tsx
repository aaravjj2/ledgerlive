interface EmptyStateProps {
  title: string
  description: string
  action?: { label: string; onClick: () => void }
  icon?: 'document' | 'exception' | 'transaction' | 'search'
}

const icons = {
  document: (
    <svg className="w-16 h-16 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
    </svg>
  ),
  exception: (
    <svg className="w-16 h-16 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
    </svg>
  ),
  transaction: (
    <svg className="w-16 h-16 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
    </svg>
  ),
  search: (
    <svg className="w-16 h-16 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
    </svg>
  ),
}

export default function EmptyState({ title, description, action, icon = 'document' }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center" data-testid="empty-state">
      {icons[icon]}
      <h3 className="mt-4 text-lg font-medium text-gray-100">{title}</h3>
      <p className="mt-2 text-sm text-gray-500 max-w-sm">{description}</p>
      {action && (
        <button
          onClick={action.onClick}
          className="mt-4 px-4 py-2 bg-red-600 text-white text-sm rounded-lg hover:bg-red-700 transition-colors"
          data-testid="empty-state-action"
        >
          {action.label}
        </button>
      )}
    </div>
  )
}
