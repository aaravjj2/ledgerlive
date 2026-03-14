/**
 * demoMode — Toggle demo mode with pre-populated data for judges.
 * When enabled, API calls can return mock data for a smooth demo experience.
 */

const DEMO_MODE_KEY = 'ledgerlive_demo_mode'

export function isDemoMode(): boolean {
  if (typeof window === 'undefined') return false
  return localStorage.getItem(DEMO_MODE_KEY) === 'true'
}

export function setDemoMode(enabled: boolean): void {
  if (typeof window === 'undefined') return
  localStorage.setItem(DEMO_MODE_KEY, enabled ? 'true' : 'false')
  window.dispatchEvent(new Event('demo-mode-change'))
}

export function toggleDemoMode(): boolean {
  const next = !isDemoMode()
  setDemoMode(next)
  return next
}
