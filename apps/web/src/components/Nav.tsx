import { NavLink, Link } from 'react-router-dom'
import clsx from 'clsx'

const links = [
  { to: '/', label: 'Dashboard', tid: 'nav-dashboard' },
  { to: '/documents', label: 'Documents', tid: 'nav-documents' },
  { to: '/reconciliation', label: 'Reconciliation', tid: 'nav-reconciliation' },
  { to: '/exceptions', label: 'Exceptions', tid: 'nav-exceptions' },
  { to: '/review', label: 'Review Queue', tid: 'nav-review' },
  { to: '/audit', label: 'Audit Log', tid: 'nav-audit' },
  { to: '/race-control', label: 'Race Control', tid: 'nav-race-control' },
  { to: '/settings', label: 'Settings', tid: 'nav-settings' },
]

export default function Nav() {
  return (
    <nav className="bg-indigo-700 text-white px-6 py-3 flex items-center gap-6 overflow-x-auto scrollbar-none" data-testid="nav-bar">
      <Link to="/" className="font-bold text-lg mr-4 flex-shrink-0 hover:text-indigo-200 transition" data-testid="app-logo">LedgerLive</Link>
      {links.map((l) => (
        <NavLink
          key={l.to}
          to={l.to}
          data-testid={l.tid}
          className={({ isActive }) =>
            clsx('text-sm hover:text-indigo-200 transition flex-shrink-0', isActive && 'underline font-semibold')
          }
        >
          {l.label}
        </NavLink>
      ))}
    </nav>
  )
}
