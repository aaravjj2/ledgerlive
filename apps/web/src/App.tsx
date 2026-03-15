import { useState, useEffect } from 'react'
import { NavLink, Link, useLocation } from 'react-router-dom'
import { routeElements } from './routes'
import SearchBar from './components/SearchBar'
import ThemeToggle from './components/ThemeToggle'
import VoiceAssistant from './components/VoiceAssistant'
import { nav } from './utils/design'
import { API_BASE } from './services/api'

// ── Agent status badge (polls every 5s) ─────────────────────────────────────
function AgentStatusBadge() {
  const [status, setStatus] = useState<'idle' | 'active'>('idle')
  useEffect(() => {
    const poll = () =>
      fetch(`${API_BASE}/api/agent/status`)
        .then(r => r.json())
        .then(d => setStatus(d?.status === 'active' ? 'active' : 'idle'))
        .catch(() => setStatus('idle'))
    poll()
    const id = setInterval(poll, 5000)
    return () => clearInterval(id)
  }, [])
  return (
    <div className="flex items-center gap-1.5 px-2 py-1 text-xs">
      <span className={`w-1.5 h-1.5 rounded-full ${status === 'active' ? 'bg-green-400 animate-pulse' : 'bg-gray-600'}`} />
      <span className={status === 'active' ? 'text-green-400' : 'text-gray-500'}>
        Agent {status === 'active' ? 'Active' : 'Idle'}
      </span>
    </div>
  )
}

// ── Sidebar nav section ──────────────────────────────────────────────────────
function SidebarSection({ section, collapsed }: { section: typeof nav.sections[0]; collapsed: boolean }) {
  const [open, setOpen] = useState(true)
  const location = useLocation()
  const isAnyActive = section.items.some(
    i => i.to === location.pathname || (i.to !== '/' && location.pathname.startsWith(i.to))
  )

  if (collapsed) {
    return (
      <div className="px-2 py-1">
        <div
          title={section.label}
          className={`flex items-center justify-center w-8 h-8 mx-auto rounded-lg text-base cursor-default
            ${isAnyActive ? 'bg-red-600/20' : 'hover:bg-[#1A1A24]'}`}
        >
          {section.icon}
        </div>
      </div>
    )
  }

  return (
    <div className="mb-1">
      <button
        onClick={() => setOpen(o => !o)}
        className="w-full flex items-center gap-2 px-3 py-1.5 text-left hover:bg-[#1A1A24] transition-colors"
      >
        <span className="text-xs">{section.icon}</span>
        <span className="text-[10px] font-bold tracking-widest text-gray-500 flex-1">{section.label}</span>
        <span className={`text-gray-600 text-xs transition-transform ${open ? 'rotate-90' : ''}`}>›</span>
      </button>
      {open && (
        <div>
          {section.items.map(item => (
            <NavLink
              key={item.tid}
              to={item.to}
              data-testid={item.tid}
              end={item.to === '/'}
              className={({ isActive }) =>
                `flex items-center gap-2 px-4 py-1.5 text-sm transition-colors ${
                  isActive
                    ? 'bg-red-600/15 border-l-2 border-red-500 text-red-300 font-medium'
                    : 'text-gray-400 hover:text-gray-200 hover:bg-[#1A1A24] border-l-2 border-transparent'
                }`
              }
            >
              <span className="truncate">{item.label}</span>
            </NavLink>
          ))}
        </div>
      )}
    </div>
  )
}

// ── Root App ─────────────────────────────────────────────────────────────────
export default function App() {
  const [collapsed, setCollapsed] = useState(false)
  const location = useLocation()

  const allItems = nav.sections.flatMap(s => s.items)
  const current = allItems.find(
    i => i.to === location.pathname || (i.to !== '/' && location.pathname.startsWith(i.to))
  )

  return (
    <div className="min-h-screen flex bg-[#0A0A0F] text-gray-100" data-testid="app-root">
      {/* ── Fixed sidebar ── */}
      <aside
        className={`fixed inset-y-0 left-0 z-30 flex flex-col bg-[#0D0D14] border-r border-[#2A2A3A] transition-all duration-200 ${
          collapsed ? 'w-14' : 'w-56'
        }`}
      >
        {/* Logo */}
        <div className="flex items-center gap-2 px-3 py-3 border-b border-[#2A2A3A]">
          <div className="w-8 h-8 bg-red-600 rounded flex items-center justify-center text-white font-bold text-xs shrink-0">
            LL
          </div>
          {!collapsed && (
            <div className="min-w-0">
              <div className="font-bold text-sm text-white leading-none">LedgerLive</div>
              <div className="text-[10px] text-gray-500 uppercase tracking-wider mt-0.5">Finance Ops</div>
            </div>
          )}
        </div>

        {/* Nav sections */}
        <nav className="flex-1 overflow-y-auto py-2 scrollbar-thin">
          {nav.sections.map(section => (
            <SidebarSection key={section.id} section={section} collapsed={collapsed} />
          ))}
        </nav>

        {/* Collapse toggle */}
        <button
          onClick={() => setCollapsed(c => !c)}
          className="flex items-center justify-center h-10 border-t border-[#2A2A3A] text-gray-500 hover:text-gray-300 hover:bg-[#1A1A24] transition-colors text-xs"
        >
          {collapsed ? '›' : '‹'}
        </button>
      </aside>

      {/* ── Content area ── */}
      <div className={`flex-1 flex flex-col min-h-screen transition-all duration-200 ${collapsed ? 'ml-14' : 'ml-56'}`}>
        {/* Sticky header */}
        <header
          className="sticky top-0 z-20 flex items-center gap-3 px-4 py-2 bg-[#0A0A0F]/95 backdrop-blur border-b border-[#2A2A3A]"
          data-testid="nav-bar"
        >
          {/* App logo (for testid compliance) */}
          <Link to="/" data-testid="app-logo" className="sr-only">LedgerLive</Link>

          {/* Breadcrumb */}
          <div className="text-sm text-gray-500">
            <span className="text-gray-600">LL</span>
            {current && (
              <>
                <span className="mx-1 text-gray-700">/</span>
                <span className="text-gray-300">{current.label}</span>
              </>
            )}
          </div>

          <div className="flex-1" />

          <SearchBar />
          <ThemeToggle dataTestId="nav-theme-toggle" />
          <AgentStatusBadge />

          <NavLink
            to="/live-voice"
            className="flex items-center gap-1.5 px-3 py-1.5 bg-red-600 hover:bg-red-700 text-white text-xs font-semibold rounded-lg transition-colors"
          >
            🎙 LedgerBot
          </NavLink>
        </header>

        {/* Main content */}
        <main className="flex-1 p-5 md:p-6" data-testid="main-content">
          {routeElements}
        </main>

        {/* Footer */}
        <footer className="text-center text-xs text-gray-600 py-2 border-t border-[#2A2A3A]" data-testid="footer">
          LedgerLive · Finance Ops Close Agent · 2026
        </footer>
      </div>

      <VoiceAssistant />
    </div>
  )
}
