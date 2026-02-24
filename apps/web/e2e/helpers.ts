/**
 * E2E Helpers — LedgerLive Playwright spec utilities
 *
 * Exports:
 *   initE2E(page)      — reset golden scenario, wait for API health
 *   seedGolden(page)   — POST /api/ops/golden-scenario-run and wait
 *   checkpoint(page, name) — screenshot with structured name
 *   pollUntil(page, testId, timeout?) — poll until testId is visible
 *   getAssertions(page) — GET /api/ops/e2e-assertions JSON
 */

import { Page, expect } from '@playwright/test'

const API = 'http://127.0.0.1:8090'

/** Reset golden scenario via backend; navigate to / to prime the session */
export async function initE2E(page: Page): Promise<void> {
  // Reset any prior golden state
  await page.request.post(`${API}/api/ops/golden-scenario-reset`)
  // Confirm API is healthy
  const health = await page.request.get(`${API}/healthz`)
  expect(health.status()).toBeLessThan(300)
}

/** Seed a deterministic golden scenario and wait for the run-status badge */
export async function seedGolden(page: Page): Promise<void> {
  // Click the Run Canonical button if on the RC page; otherwise call API directly
  const runBtn = page.getByTestId('race-control-run-golden')
  const isRCPage = await runBtn.isVisible({ timeout: 2000 }).catch(() => false)

  if (isRCPage) {
    await runBtn.click()
    await expect(page.getByTestId('rc-run-status')).toBeVisible({ timeout: 15_000 })
  } else {
    await page.request.post(`${API}/api/ops/golden-scenario-run`)
  }
}

/** Take a named screenshot checkpoint for the proof pack */
export async function checkpoint(page: Page, name: string): Promise<void> {
  await page.screenshot({
    path: `playwright-report/screenshots/${name}.png`,
    fullPage: false,
  })
}

/** Poll until a data-testid is visible, with optional timeout (default 10s) */
export async function pollUntil(
  page: Page,
  testId: string,
  timeout = 10_000
): Promise<void> {
  await expect(page.getByTestId(testId)).toBeVisible({ timeout })
}

/** GET /api/ops/e2e-assertions and return the parsed JSON */
export async function getAssertions(page: Page): Promise<Record<string, unknown>> {
  const resp = await page.request.get(`${API}/api/ops/e2e-assertions`)
  expect(resp.ok()).toBeTruthy()
  return resp.json()
}

/** Navigate to a given path and wait for the primary testId to be visible */
export async function gotoPage(
  page: Page,
  path: string,
  testId: string,
  timeout = 15_000
): Promise<void> {
  await page.goto(path)
  await expect(page.getByTestId(testId)).toBeVisible({ timeout })
}
