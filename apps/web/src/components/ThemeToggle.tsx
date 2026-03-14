/**
 * ThemeToggle — Switch between light, dark, and terminal (Bloomberg) themes.
 */
import { useEffect, useState } from 'react'
import { getStoredTheme, setStoredTheme, type ThemeMode } from '../utils/theme'

interface ThemeToggleProps {
  className?: string
  dataTestId?: string
}

function ThemeToggle({ className = '', dataTestId }: ThemeToggleProps) {
  const [theme, setTheme] = useState<ThemeMode>(getStoredTheme)

  useEffect(() => {
    setStoredTheme(theme)
  }, [theme])

  const cycle = () => {
    const next: ThemeMode = theme === 'light' ? 'dark' : theme === 'dark' ? 'terminal' : 'light'
    setTheme(next)
  }

  return (
    <button
      data-testid={dataTestId ?? 'theme-toggle'}
      onClick={cycle}
      className={`px-3 py-1.5 rounded-lg text-sm font-medium border border-gray-300 dark:border-gray-600 hover:bg-gray-100 dark:hover:bg-gray-700 transition ${className}`}
      title={`Current: ${theme}. Click to cycle.`}
    >
      {theme === 'light' && '☀️ Light'}
      {theme === 'dark' && '🌙 Dark'}
      {theme === 'terminal' && '🖥️ Terminal'}
    </button>
  )
}

export default ThemeToggle
