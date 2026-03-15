/**
 * LedgerLive Design System
 * F1-inspired dark finance SaaS — "Linear meets Rippling meets F1 timing screen"
 */

export const colors = {
  bg: {
    base: '#0A0A0F',
    surface: '#111118',
    elevated: '#1A1A24',
    border: '#2A2A3A',
  },
  brand: {
    red: '#E8002D',
    redHover: '#FF1744',
    blue: '#00D2FF',
    blueHover: '#40E0FF',
    gold: '#FFD700',
  },
  status: {
    success: '#00C853',
    warning: '#FFB300',
    danger: '#E8002D',
    info: '#00D2FF',
    neutral: '#6B7280',
  },
  text: {
    primary: '#F8F9FA',
    secondary: '#9CA3AF',
    muted: '#6B7280',
    inverse: '#0A0A0F',
  },
}

// All nav sections — includes every data-testid that existed in the old Nav.tsx
export const nav = {
  sections: [
    {
      id: 'command',
      label: 'Command',
      icon: '🏎️',
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
      id: 'close',
      label: 'Close Cycle',
      icon: '🔄',
      items: [
        { to: '/documents',       label: 'Documents',       tid: 'nav-documents' },
        { to: '/ocr',             label: 'OCR Pipeline',    tid: 'nav-ocr' },
        { to: '/reconciliation',  label: 'Reconciliation',  tid: 'nav-reconciliation' },
        { to: '/bank-recon',      label: 'Bank Recon',      tid: 'nav-bank-recon' },
        { to: '/three-way-match', label: '3-Way Match',     tid: 'nav-three-way-match' },
        { to: '/exceptions',      label: 'Exceptions',      tid: 'nav-exceptions' },
        { to: '/review',          label: 'Review Queue',    tid: 'nav-review' },
        { to: '/approvals',       label: 'Approvals',       tid: 'nav-approvals' },
        { to: '/close-period',    label: 'Close Period',    tid: 'nav-close-period' },
      ],
    },
    {
      id: 'ledger',
      label: 'General Ledger',
      icon: '📒',
      items: [
        { to: '/journal-entries',    label: 'Journal Entries', tid: 'nav-journal' },
        { to: '/je-posting',         label: 'JE Posting',      tid: 'nav-je-posting' },
        { to: '/trial-balance',      label: 'Trial Balance',   tid: 'nav-trial-balance' },
        { to: '/chart-of-accounts',  label: 'Chart of Accounts', tid: 'nav-coa' },
        { to: '/accruals',           label: 'Accruals',        tid: 'nav-accruals' },
        { to: '/financial-statements', label: 'Financials',    tid: 'nav-financials' },
      ],
    },
    {
      id: 'ar-ap',
      label: 'AR / AP',
      icon: '💳',
      items: [
        { to: '/invoices',         label: 'Invoices',          tid: 'nav-invoices' },
        { to: '/payments',         label: 'Payments',          tid: 'nav-payments' },
        { to: '/vendors',          label: 'Vendors',           tid: 'nav-vendors' },
        { to: '/expenses',         label: 'Expenses',          tid: 'nav-expenses' },
        { to: '/cash-application', label: 'Cash Application',  tid: 'nav-cash-app' },
        { to: '/revenue',          label: 'Revenue',           tid: 'nav-revenue' },
      ],
    },
    {
      id: 'consolidation',
      label: 'Consolidation',
      icon: '🌐',
      items: [
        { to: '/consolidation',    label: 'Consolidation',     tid: 'nav-consolidation' },
        { to: '/intercompany-v2',  label: 'Intercompany',      tid: 'nav-intercompany' },
        { to: '/fx',               label: 'FX / Currency',     tid: 'nav-fx' },
        { to: '/cashflow-consol',  label: 'Cash Flow',         tid: 'nav-cashflow' },
        { to: '/entities',         label: 'Entities',          tid: 'nav-entities' },
      ],
    },
    {
      id: 'fpa',
      label: 'FP&A',
      icon: '📈',
      items: [
        { to: '/budgeting',        label: 'Budgeting',         tid: 'nav-budgeting' },
        { to: '/forecasting',      label: 'Forecasting',       tid: 'nav-forecasting' },
        { to: '/scenario-engine',  label: 'Scenarios',         tid: 'nav-scenarios' },
        { to: '/driver-planning',  label: 'Driver Planning',   tid: 'nav-driver-planning' },
        { to: '/kpi',              label: 'KPIs',              tid: 'nav-kpi' },
        { to: '/board-pack',       label: 'Board Pack',        tid: 'nav-board-pack' },
      ],
    },
    {
      id: 'compliance',
      label: 'Compliance',
      icon: '🛡️',
      items: [
        { to: '/compliance',       label: 'Compliance',        tid: 'nav-compliance' },
        { to: '/controls',         label: 'Controls',          tid: 'nav-controls' },
        { to: '/soc2',             label: 'SOC 2',             tid: 'nav-soc2' },
        { to: '/audit',            label: 'Audit Log',         tid: 'nav-audit' },
        { to: '/evidence-binder',  label: 'Evidence',          tid: 'nav-evidence' },
        { to: '/audit-portal',     label: 'Audit Portal',      tid: 'nav-audit-portal' },
      ],
    },
    {
      id: 'ai',
      label: 'AI & Agents',
      icon: '🤖',
      items: [
        { to: '/multi-agent',      label: 'Multi-Agent',       tid: 'nav-multi-agent' },
        { to: '/agent-console',    label: 'Agent Console',     tid: 'nav-agent-console' },
        { to: '/gradient-ai',      label: 'Gradient AI',       tid: 'nav-gradient-ai' },
        { to: '/airia-everywhere', label: 'Airia Everywhere',  tid: 'nav-airia-everywhere' },
        { to: '/airia',            label: 'Airia Readiness',   tid: 'nav-airia' },
        { to: '/blueprint-builder',label: 'Blueprint Builder', tid: 'nav-blueprint' },
        { to: '/trace-explorer',   label: 'Trace Explorer',    tid: 'nav-trace' },
      ],
    },
    {
      id: 'integrations',
      label: 'Integrations',
      icon: '🔌',
      items: [
        { to: '/connectors',       label: 'Connectors',        tid: 'nav-connectors' },
        { to: '/qbo',              label: 'QuickBooks',        tid: 'nav-qbo' },
        { to: '/xero',             label: 'Xero',              tid: 'nav-xero' },
        { to: '/plaid',            label: 'Plaid',             tid: 'nav-plaid' },
        { to: '/bloomberg',        label: 'Bloomberg',         tid: 'nav-bloomberg' },
        { to: '/treasury',         label: 'Treasury',          tid: 'nav-treasury' },
      ],
    },
    {
      id: 'showcase',
      label: 'Showcase',
      icon: '✨',
      items: [
        { to: '/showcase',         label: 'Hackathon',         tid: 'nav-showcase' },
        { to: '/storyteller',      label: 'Storyteller',       tid: 'nav-storyteller' },
        { to: '/ui-navigator',     label: 'UI Navigator',      tid: 'nav-ui-navigator' },
      ],
    },
    {
      id: 'admin',
      label: 'Admin',
      icon: '⚙️',
      items: [
        { to: '/users',            label: 'Users',             tid: 'nav-users' },
        { to: '/roles',            label: 'Roles',             tid: 'nav-roles' },
        { to: '/settings',         label: 'Settings',          tid: 'nav-settings' },
        { to: '/notifications',    label: 'Notifications',     tid: 'nav-notifications' },
        { to: '/admin-console',    label: 'Admin Console',     tid: 'nav-admin' },
      ],
    },
  ],
}
