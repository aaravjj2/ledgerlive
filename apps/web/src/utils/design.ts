/**
 * LedgerLive Design System — F1 dark theme brand tokens and navigation structure.
 */

export const colors = {
  bg: {
    base:     '#0A0A0F',
    surface:  '#111118',
    elevated: '#1A1A24',
    border:   '#2A2A3A',
  },
  brand: {
    red:      '#E8002D',
    redHover: '#FF1744',
    blue:     '#00D2FF',
    gold:     '#FFD700',
  },
  status: {
    success: '#00C853',
    warning: '#FFB300',
    danger:  '#E8002D',
    info:    '#00D2FF',
  },
  text: {
    primary:   '#F8F9FA',
    secondary: '#9CA3AF',
    muted:     '#6B7280',
  },
} as const

export interface NavItem {
  to: string
  label: string
  tid: string
}

export interface NavSection {
  id: string
  label: string
  icon: string
  items: NavItem[]
}

export const nav: { sections: NavSection[] } = {
  sections: [
    {
      id: 'command', label: 'COMMAND', icon: '🏎️',
      items: [
        { to: '/',                label: 'Pit Lane',        tid: 'nav-dashboard' },
        { to: '/race-control',    label: 'Race Control',    tid: 'nav-race-control' },
        { to: '/cfo-cockpit',     label: 'CFO Cockpit',     tid: 'nav-cfo-cockpit' },
        { to: '/live-voice',      label: 'LedgerBot',       tid: 'nav-live-voice' },
        { to: '/close-calendar',  label: 'Close Calendar',  tid: 'nav-close-calendar' },
        { to: '/close-scorecard', label: 'Scorecard',       tid: 'nav-close-scorecard' },
      ],
    },
    {
      id: 'close', label: 'CLOSE CYCLE', icon: '📋',
      items: [
        { to: '/documents',     label: 'Documents',     tid: 'nav-documents' },
        { to: '/reconciliation',label: 'Reconciliation',tid: 'nav-reconciliation' },
        { to: '/exceptions',    label: 'Exceptions',    tid: 'nav-exceptions' },
        { to: '/review',        label: 'Review Queue',  tid: 'nav-review' },
        { to: '/audit',         label: 'Audit Log',     tid: 'nav-audit' },
      ],
    },
    {
      id: 'integrations', label: 'INTEGRATIONS', icon: '🔌',
      items: [
        { to: '/connectors', label: 'Connectors', tid: 'nav-connectors' },
        { to: '/treasury',   label: 'Treasury',   tid: 'nav-treasury' },
        { to: '/ocr',        label: 'OCR',        tid: 'nav-ocr' },
      ],
    },
    {
      id: 'compliance', label: 'COMPLIANCE', icon: '🛡️',
      items: [
        { to: '/compliance', label: 'Compliance', tid: 'nav-compliance' },
        { to: '/bloomberg',  label: 'Terminal',   tid: 'nav-bloomberg' },
      ],
    },
    {
      id: 'ai', label: 'AI & AGENTS', icon: '🤖',
      items: [
        { to: '/multi-agent',      label: 'Multi-Agent',     tid: 'nav-multi-agent' },
        { to: '/agent-console',    label: 'Agent Console',   tid: 'nav-agent-console' },
        { to: '/airia',            label: 'Airia',           tid: 'nav-airia' },
        { to: '/airia-everywhere', label: 'Airia Everywhere',tid: 'nav-airia-everywhere' },
        { to: '/gradient-ai',      label: 'Gradient AI',     tid: 'nav-gradient-ai' },
        { to: '/storyteller',      label: 'Storyteller',     tid: 'nav-storyteller' },
      ],
    },
    {
      id: 'showcase', label: 'SHOWCASE', icon: '🏆',
      items: [
        { to: '/showcase',     label: 'Hackathon',    tid: 'nav-showcase' },
        { to: '/ui-navigator', label: 'UI Navigator', tid: 'nav-ui-navigator' },
      ],
    },
    {
      id: 'admin', label: 'ADMIN', icon: '⚙️',
      items: [
        { to: '/settings', label: 'Settings', tid: 'nav-settings' },
      ],
    },
  ],
}
