import { NavLink, Link } from 'react-router-dom'
import clsx from 'clsx'
import ThemeToggle from './ThemeToggle'
import SearchBar from './SearchBar'

const links = [
  { to: '/', label: 'Dashboard', tid: 'nav-dashboard' },
  { to: '/showcase', label: '🏆 Hackathon', tid: 'nav-showcase' },
  { to: '/cfo-cockpit', label: 'CFO Cockpit', tid: 'nav-cfo-cockpit' },
  { to: '/live-voice', label: 'Live Voice', tid: 'nav-live-voice' },
  { to: '/storyteller', label: 'Storyteller', tid: 'nav-storyteller' },
  { to: '/ui-navigator', label: 'UI Navigator', tid: 'nav-ui-navigator' },
  { to: '/gradient-ai', label: 'Gradient AI', tid: 'nav-gradient-ai' },
  { to: '/airia-everywhere', label: 'Airia Everywhere', tid: 'nav-airia-everywhere' },
  { to: '/multi-agent', label: 'Multi-Agent', tid: 'nav-multi-agent' },
  { to: '/bloomberg', label: 'Terminal', tid: 'nav-bloomberg' },
  { to: '/documents', label: 'Documents', tid: 'nav-documents' },
  { to: '/reconciliation', label: 'Reconciliation', tid: 'nav-reconciliation' },
  { to: '/exceptions', label: 'Exceptions', tid: 'nav-exceptions' },
  { to: '/review', label: 'Review Queue', tid: 'nav-review' },
  { to: '/close-calendar', label: 'Close Calendar', tid: 'nav-close-calendar' },
  { to: '/connectors', label: 'Connectors', tid: 'nav-connectors' },
  { to: '/treasury', label: 'Treasury', tid: 'nav-treasury' },
  { to: '/compliance', label: 'Compliance', tid: 'nav-compliance' },
  { to: '/ocr', label: 'OCR', tid: 'nav-ocr' },
  { to: '/close-scorecard', label: 'Scorecard', tid: 'nav-close-scorecard' },
  { to: '/audit', label: 'Audit Log', tid: 'nav-audit' },
  { to: '/race-control', label: 'Race Control', tid: 'nav-race-control' },
  { to: '/agent-console', label: 'Agent', tid: 'nav-agent-console' },
  { to: '/airia', label: 'Airia', tid: 'nav-airia' },
  { to: '/settings', label: 'Settings', tid: 'nav-settings' },
]

export default function Nav() {
  return (
    <nav className="bg-red-700 text-white px-6 py-3 flex items-center gap-6 overflow-x-auto scrollbar-none" data-testid="nav-bar">
      <Link to="/" className="font-bold text-lg mr-4 flex-shrink-0 hover:text-indigo-200 transition" data-testid="app-logo">LedgerLive</Link>
      <SearchBar />
      <ThemeToggle dataTestId="nav-theme-toggle" />
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
