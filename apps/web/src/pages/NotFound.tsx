import { Link } from 'react-router-dom'

export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] text-center" data-testid="page-not-found">
      <div className="text-7xl mb-4">🚫</div>
      <h1 className="text-4xl font-bold text-gray-800 mb-2">404</h1>
      <p className="text-gray-500 mb-6 text-lg">Page not found.</p>
      <Link
        to="/"
        className="px-5 py-2 rounded-lg bg-indigo-600 text-white font-medium hover:bg-indigo-700 transition-colors"
        data-testid="not-found-home-link"
      >
        ← Back to Dashboard
      </Link>
    </div>
  )
}
