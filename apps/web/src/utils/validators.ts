/**
 * Validators — Input validation for forms and API payloads.
 */

export function isNonEmptyString(s: unknown): s is string {
  return typeof s === 'string' && s.trim().length > 0
}

export function isValidEmail(s: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(s)
}

export function isValidAmount(n: unknown): n is number {
  return typeof n === 'number' && !Number.isNaN(n) && isFinite(n)
}

export function isValidId(s: unknown): s is string {
  return typeof s === 'string' && /^[a-zA-Z0-9_-]+$/.test(s) && s.length <= 64
}

export function isValidDate(s: string): boolean {
  const d = new Date(s)
  return !Number.isNaN(d.getTime())
}

export function clamp(value: number, min: number, max: number): number {
  return Math.min(max, Math.max(min, value))
}
