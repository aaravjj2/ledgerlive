/**
 * Keyboard — Shortcuts for power-user navigation (Bloomberg-style).
 */

export type KeyCombo = { key: string; ctrl?: boolean; alt?: boolean; shift?: boolean }

export function matchKeyCombo(e: KeyboardEvent, combo: KeyCombo): boolean {
  const keyMatch = e.key.toLowerCase() === combo.key.toLowerCase()
  const ctrlMatch = combo.ctrl ? (e.ctrlKey || e.metaKey) : !(e.ctrlKey || e.metaKey)
  const altMatch = combo.alt ? e.altKey : !e.altKey
  const shiftMatch = combo.shift ? e.shiftKey : !e.shiftKey
  return keyMatch && ctrlMatch && altMatch && shiftMatch
}

export function formatCombo(combo: KeyCombo): string {
  const parts: string[] = []
  if (combo.ctrl) parts.push('Ctrl')
  if (combo.alt) parts.push('Alt')
  if (combo.shift) parts.push('Shift')
  parts.push(combo.key.toUpperCase())
  return parts.join('+')
}

export const DEFAULT_SHORTCUTS: Record<string, KeyCombo> = {
  dashboard: { key: 'd', ctrl: true },
  raceControl: { key: 'r', ctrl: true },
  documents: { key: 'o', ctrl: true },
  exceptions: { key: 'e', ctrl: true },
  refresh: { key: 'r', ctrl: true, shift: true },
}
