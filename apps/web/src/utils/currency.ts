/**
 * Currency formatting and parsing utilities for finance close.
 */
export const CURRENCY_SYMBOLS: Record<string, string> = {
  USD: '$',
  EUR: '€',
  GBP: '£',
  JPY: '¥',
  INR: '₹',
}

export function formatCurrency(
  value: number,
  currency: string = 'USD',
  options?: Intl.NumberFormatOptions
): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
    ...options,
  }).format(value)
}

export function formatCompact(value: number): string {
  if (Math.abs(value) >= 1_000_000) return (value / 1_000_000).toFixed(1) + 'M'
  if (Math.abs(value) >= 1_000) return (value / 1_000).toFixed(1) + 'K'
  return value.toFixed(2)
}

export function parseCurrency(input: string): number {
  const cleaned = input.replace(/[^0-9.-]/g, '')
  return parseFloat(cleaned) || 0
}

export function formatPercent(value: number, decimals: number = 1): string {
  return `${value.toFixed(decimals)}%`
}
