/**
 * Theme utilities for LedgerLive — supports dark (Bloomberg-style) and light modes.
 * Used across Terminal, Dashboard, and hackathon demo views.
 */

export type ThemeMode = 'light' | 'dark' | 'terminal'

export const THEME_STORAGE_KEY = 'ledgerlive-theme'

export function getStoredTheme(): ThemeMode {
  if (typeof window === 'undefined') return 'dark'
  const stored = localStorage.getItem(THEME_STORAGE_KEY) as ThemeMode | null
  return stored && ['light', 'dark', 'terminal'].includes(stored) ? stored : 'dark'
}

export function setStoredTheme(mode: ThemeMode): void {
  if (typeof window === 'undefined') return
  localStorage.setItem(THEME_STORAGE_KEY, mode)
  document.documentElement.classList.remove('theme-light', 'theme-dark', 'theme-terminal', 'dark')
  document.documentElement.classList.add(`theme-${mode}`)
  // Add Tailwind 'dark' class for dark: variants
  if (mode === 'dark' || mode === 'terminal') {
    document.documentElement.classList.add('dark')
  }
}

export function applyTheme(mode: ThemeMode): void {
  setStoredTheme(mode)
}

export const TERMINAL_COLORS = {
  bg: '#0d1117',
  surface: '#161b22',
  border: '#30363d',
  text: '#c9d1d9',
  textMuted: '#8b949e',
  accent: '#58a6ff',
  success: '#3fb950',
  warning: '#d29922',
  error: '#f85149',
  green: '#238636',
  red: '#da3633',
} as const

export const LIGHT_COLORS = {
  bg: '#ffffff',
  surface: '#f6f8fa',
  border: '#d0d7de',
  text: '#1f2328',
  textMuted: '#656d76',
  accent: '#0969da',
  success: '#1a7f37',
  warning: '#9a6700',
  error: '#cf222e',
  green: '#1a7f37',
  red: '#cf222e',
} as const
