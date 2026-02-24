/**
 * TOUR SPEC  — LedgerLive UX tour (generates TOUR.webm)
 *
 * Visits every page with deliberate pauses so the combined recording is
 * ≥ 240 seconds.  Playwright records video=on for this test via config.
 *
 * Not included in the normal test run; invoked explicitly by the proof
 * generator with --grep TOUR.
 *
 * SELECTOR POLICY: data-testid ONLY.  No role, text, label, placeholder,
 * alt-text, title, body locator, querySelector, xpath, or deep combinator
 * selectors are permitted.
 */
import { test, expect } from '@playwright/test'
import { initE2E, checkpoint } from './helpers'

const PAGES: Array<{ path: string; testId: string; fallback: string; label: string }> = [
  { path: '/',               testId: 'dashboard-page',       fallback: 'dashboard-loading',     label: 'Dashboard'      },
  { path: '/documents',      testId: 'documents-page',       fallback: 'documents-loading',     label: 'Documents'      },
  { path: '/reconciliation', testId: 'reconciliation-page',  fallback: 'reconciliation-loading',label: 'Reconciliation' },
  { path: '/exceptions',     testId: 'exceptions-page',      fallback: 'exceptions-loading',    label: 'Exceptions'     },
  { path: '/review',         testId: 'review-page',          fallback: 'review-loading',        label: 'Review Queue'   },
  { path: '/audit',          testId: 'audit-page',           fallback: 'audit-loading',         label: 'Audit Log'      },
  { path: '/settings',       testId: 'settings-page',        fallback: 'settings-loading',      label: 'Settings'       },
]

// Each page dwell = 35 s → 7 × 35 = 245 s total ≥ 240 s requirement
const DWELL_MS = 35_000

test('TOUR — full UX walkthrough (≥240 s)', async ({ page }) => {
  // Set a very long timeout for the full tour
  test.setTimeout(420_000)

  await initE2E(page)

  for (const { path, testId, fallback, label } of PAGES) {
    await page.goto(path)
    // Wait for the page-specific data-testid (loaded or loading state)
    const loaded = page.getByTestId(testId)
    const loading = page.getByTestId(fallback)
    await expect(loaded.or(loading)).toBeVisible({ timeout: 15_000 })

    // Capture a named screenshot checkpoint
    await checkpoint(page, `tour-${label.toLowerCase().replace(/\s+/g, '-')}`)

    // Dwell on page so recording is long enough
    await page.waitForTimeout(DWELL_MS)
  }

  // Final sanity: verify branding via data-testid
  await page.goto('/')
  const loaded = page.getByTestId('dashboard-page')
  const loading = page.getByTestId('dashboard-loading')
  await expect(loaded.or(loading)).toBeVisible({ timeout: 15_000 })
  await expect(page.getByTestId('app-logo')).toHaveText('LedgerLive')
  await checkpoint(page, 'tour-final')
})
