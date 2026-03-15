/**
 * LedgerLive App Shell — F1-inspired dark finance SaaS layout
 * Sidebar + top header bar + main content area
 */
import { useState, useEffect, useCallback } from 'react'
import { NavLink, Link, useLocation } from 'react-router-dom'
import { routeElements } from './routes'
import VoiceAssistant from './components/VoiceAssistant'
import ThemeToggle from './components/ThemeToggle'
import SearchBar from './components/SearchBar'
import { nav } from './utils/design'
import { API_BASE } from './services/api'

// ── Agent status badge ─────────────────────────────────────────────────────────
function AgentStatusBadge() {
  const [status, setStatus] = useState<'idle' | 'running' | 'review' | 'error'>('idle')

  useEffect(() => {
    const poll = () =>
      fetch(`${API_BASE}/api/agent/status`)
        .then(r => r.json())
        .then(d => setStatus(d.status || 'idle'))
        .catch(() => setStatus('idle'))
    poll()
    const t = setInterval(poll, 5000)
    return () => clearInterval(t)
  }, [])

  const map = {
    idle:    { label: 'Agent Idle',    dot: 'bg-gray-500',                    text: 'text-gray-500' },
    running: { label: 'Agent Running', dot: 'bg-blue-400 animate-pulse',      text: 'text-blue-400' },
    review:  { label: 'Needs Review',  dot: 'bg-yellow-400 animate-pulse',    text: 'text-yellow-400' },
    error:   { label: 'Agent Error',   dot: 'bg-red-500',                     text: 'text-red-400' },
  }
  const s = map[status]
  return (
    <div className="flex items-center gap-1.5 px-2 py-1.5 rounded-lg bg-white/5 border border-white/8">
      <span className={`w-1.5 h-1.5 rounded-full flex-shrink-0 ${s.dot}`} />
      <span className={`text-xs font-mono truncate ${s.text}`}>{s.label}</span>
    </div>
  )
}

// ── Sidebar nav section ────────────────────────────────────────────────────────
type NavItem = { to: string; label: string; tid: string }
type Section = { id: string; label: string; icon: string; items: NavItem[] }

function NavSection({ section, collapsed }: { section: Section; collapsed: boolean }) {
  const location = useLocation()
  const isAnyActive = section.items.some(i =>
    i.to === '/' ? location.pathname === '/' : location.pathname.startsWith(i.to)
  )
  const [open, setOpen] = useState(isAnyActive)

  if (collapsed) {
    return (
      <div className="px-1.5 py-1">
        <div
          title={section.label}
          className="flex items-center justify-center w-9 h-7 rounded text-base text-gray-500 cursor-default select-none"
        >
          {section.icon}
        </div>
        {section.items.slice(0, 4).map(item => (
          <NavLink
            key={item.to}
            to={item.to}
            data-testid={item.tid}
            title={item.label}
            end={item.to === '/'}
            className={({ isActive }) =>
              `flex items-center justify-center w-9 h-8 rounded-lg mb-0.5 text-sm transition-all
               ${isActive
                 ? 'bg-red-600/20 text-red-400'
                 : 'text-gray-600 hover:text-gray-200 hover:bg-white/5'}`
            }
          >
            {item.label.slice(0, 2)}
          </NavLink>
        ))}
      </div>
    )
  }

  return (
    <div className="mb-0.5">
      <button
        onClick={() => setOpen(o => !o)}
        className={`w-full flex items-center justify-between px-3 py-1.5 rounded-md text-xs font-semibold uppercase tracking-widest transition-colors
          ${isAnyActive ? 'text-gray-300' : 'text-gray-600 hover:text-gray-400'}`}
      >
        <span className="flex items-center gap-2">
          <span className="text-sm">{section.icon}</span>
          <span>{section.label}</span>
        </span>
        <span className={`transition-transform text-gray-700 text-xs ${open ? 'rotate-90' : ''}`}>›</span>
      </button>
      {open && (
        <div className="ml-1 mt-0.5">
          {section.items.map(item => (
            <NavLink
              key={item.to}
              to={item.to}
              data-testid={item.tid}
              end={item.to === '/'}
              className={({ isActive }) =>
                `flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm transition-all mb-0.5
                 ${isActive
                   ? 'bg-red-600/15 text-red-300 font-medium border-l-2 border-red-500 !pl-[10px]'
                   : 'text-gray-500 hover:text-gray-200 hover:bg-white/5'}`
              }
            >
              {item.label}
            </NavLink>
          ))}
        </div>
      )}
    </div>
  )
}

// ── App root ───────────────────────────────────────────────────────────────────
export default function App() {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)
  const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false)
  const location = useLocation()

  // Close mobile sidebar on navigate
  useEffect(() => { setMobileSidebarOpen(false) }, [location.pathname])

  const currentPage = nav.sections
    .flatMap(s => s.items)
    .find(i => i.to === '/' ? location.pathname === '/' : location.pathname.startsWith(i.to))

  const toggleSidebar = useCallback(() => setSidebarCollapsed(c => !c), [])

  return (
    <div className="min-h-screen bg-[#0A0A0F] text-gray-100 flex" data-testid="app-root">

      {/* Mobile overlay */}
      {mobileSidebarOpen && (
        <div
          className="fixed inset-0 bg-black/70 z-20 lg:hidden"
          onClick={() => setMobileSidebarOpen(false)}
        />
      )}

      {/* ── SIDEBAR ── */}
      <aside
        className={`
          fixed top-0 left-0 h-full z-30 flex flex-col
          bg-[#0D0D14] border-r border-[#1E1E2E]
          transition-all duration-200 ease-in-out
          ${sidebarCollapsed ? 'w-14' : 'w-56'}
          ${mobileSidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
        `}
        data-testid="sidebar"
      >
        {/* Logo + collapse toggle */}
        <div className={`flex items-center border-b border-[#1E1E2E] flex-shrink-0 ${sidebarCollapsed ? 'justify-center px-2 py-4' : 'px-3 py-4 justify-between'}`}>
          {!sidebarCollapsed && (
            <Link to="/" className="flex items-center gap-2 min-w-0" data-testid="app-logo">
              <span className="text-red-500 text-base flex-shrink-0">🏎️</span>
              <div className="min-w-0">
                <div className="font-bold text-white text-sm tracking-wide truncate">LedgerLive</div>
                <div className="text-[10px] text-gray-600 font-mono tracking-wider truncate">FINANCE OPS</div>
              </div>
            </Link>
          )}
          {sidebarCollapsed && (
            <Link to="/" data-testid="app-logo" title="LedgerLive">
              <span className="text-red-500 text-lg">🏎️</span>
            </Link>
          )}
          <button
            onClick={toggleSidebar}
            className="hidden lg:flex p-1 rounded hover:bg-white/5 text-gray-600 hover:text-gray-300 transition flex-shrink-0"
            data-testid="sidebar-collapse-btn"
            title={sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
          >
            <span className="text-sm font-mono">{sidebarCollapsed ? '›' : '‹'}</span>
          </button>
        </div>

        {/* Scrollable nav sections */}
        <nav className="flex-1 overflow-y-auto py-2 scrollbar-thin scrollbar-track-transparent scrollbar-thumb-gray-700">
          {nav.sections.map(section => (
            <NavSection key={section.id} section={section} collapsed={sidebarCollapsed} />
          ))}
          {/* Bottom padding spacer */}
          <div className="h-4" />
        </nav>

        {/* Agent status — bottom of sidebar */}
        {!sidebarCollapsed && (
          <div className="p-3 border-t border-[#1E1E2E] flex-shrink-0">
            <AgentStatusBadge />
          </div>
        )}
      </aside>

      {/* ── MAIN AREA ── */}
      <div className={`flex-1 flex flex-col min-h-screen transition-all duration-200 ${sidebarCollapsed ? 'lg:ml-14' : 'lg:ml-56'}`}>

        {/* TOP HEADER */}
        <header
          className="sticky top-0 z-10 flex items-center gap-3 px-4 py-2.5 bg-[#0A0A0F]/95 backdrop-blur-sm border-b border-[#1E1E2E]"
          data-testid="nav-bar"
        >
          {/* Mobile hamburger */}
          <button
            onClick={() => setMobileSidebarOpen(o => !o)}
            className="flex lg:hidden p-1.5 rounded hover:bg-white/5 text-gray-500 hover:text-gray-300 transition"
            data-testid="mobile-menu-btn"
          >
            <span className="text-lg leading-none">☰</span>
          </button>

          {/* Breadcrumb */}
          <div className="flex items-center gap-1.5 flex-1 min-w-0 text-sm">
            <span className="text-gray-700 hidden sm:block font-mono text-xs">LL</span>
            <span className="text-gray-700 hidden sm:block">/</span>
            <span className="text-gray-300 font-medium truncate">
              {currentPage?.label ?? 'Dashboard'}
            </span>
          </div>

          {/* Search */}
          <SearchBar />

          {/* Theme toggle */}
          <ThemeToggle dataTestId="nav-theme-toggle" />

          {/* LedgerBot quick access */}
          <NavLink
            to="/live-voice"
            data-testid="nav-live-voice-header"
            className="hidden sm:flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-red-600/10 border border-red-500/25 text-red-400 hover:bg-red-600/20 transition text-xs font-medium flex-shrink-0"
          >
            🎙️ <span className="hidden md:inline">LedgerBot</span>
          </NavLink>
        </header>

        {/* PAGE CONTENT */}
        <main className="flex-1 p-5 md:p-6" data-testid="main-content">
          {routeElements}
        </main>

        {/* FOOTER */}
        <footer className="text-center text-xs text-gray-800 py-2.5 border-t border-[#1E1E2E] font-mono" data-testid="footer">
          LedgerLive · Finance Ops Close Agent · {new Date().getFullYear()}
        </footer>
      </div>

      {/* Floating voice assistant */}
      <VoiceAssistant />
    </div>
  )
}
