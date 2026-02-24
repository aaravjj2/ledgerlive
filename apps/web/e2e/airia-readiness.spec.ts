/**
 * airia-readiness.spec.ts
 *
 * Airia Readiness — E2E walkthrough of the /airia page.
 * Validates: page loads, bundle hash present, generate/validate/verify all PASS,
 * tools list rendered, F1 theme badge visible on Race Control.
 *
 * SELECTOR POLICY: data-testid ONLY.
 */
import { test, expect } from '@playwright/test'
import { checkpoint } from './helpers'

const API = 'http://127.0.0.1:8090'

test.describe('Airia Readiness', () => {
  test('AR-01 — /airia page loads with bundle hash and validator badge', async ({ page }) => {
    await page.goto('/airia')
    const pg = page.getByTestId('airia-readiness-page')
    await expect(pg).toBeVisible({ timeout: 10_000 })

    // Validator badge must show PASS or status
    const badge = page.getByTestId('airia-validator-badge')
    await expect(badge).toBeVisible({ timeout: 8_000 })

    // Bundle hash must be non-empty (API loaded)
    const bundleHash = page.getByTestId('airia-bundle-hash')
    await expect(bundleHash).toBeVisible({ timeout: 8_000 })
    const hashText = await bundleHash.textContent()
    expect(hashText?.trim().length).toBeGreaterThan(10)

    await checkpoint(page, 'AR-01-airia-readiness-page')
  })

  test('AR-02 — generate bundle returns hash', async ({ page }) => {
    await page.goto('/airia')
    await expect(page.getByTestId('airia-readiness-page')).toBeVisible({ timeout: 10_000 })

    // Click Generate
    await page.getByTestId('airia-generate-btn').click()

    // Bundle hash field should update
    const bundleHash = page.getByTestId('airia-bundle-hash')
    await expect(bundleHash).not.toHaveText('loading…', { timeout: 8_000 })
    const text = await bundleHash.textContent()
    expect(text?.trim().length).toBeGreaterThan(10)

    await checkpoint(page, 'AR-02-airia-generate-bundle')
  })

  test('AR-03 — validate bundle returns PASS', async ({ page }) => {
    await page.goto('/airia')
    await expect(page.getByTestId('airia-readiness-page')).toBeVisible({ timeout: 10_000 })

    // Click Validate
    await page.getByTestId('airia-validate-btn').click()

    // The validator badge (in page) should show PASS
    const badge = page.getByTestId('airia-validator-badge')
    await expect(badge).toHaveText('PASS', { timeout: 10_000 })

    // Also the inline result should show PASS
    const status = page.getByTestId('airia-verify-status')
    await expect(status).toHaveText('PASS', { timeout: 10_000 })

    await checkpoint(page, 'AR-03-airia-validate-pass')
  })

  test('AR-04 — tools list shows 8 Airia tools', async ({ page }) => {
    await page.goto('/airia')
    await expect(page.getByTestId('airia-readiness-page')).toBeVisible({ timeout: 10_000 })

    // Tools list must have 8 items
    const toolsList = page.getByTestId('airia-tools-list')
    await expect(toolsList).toBeVisible({ timeout: 8_000 })
    const items = toolsList.locator('li')
    await expect(items).toHaveCount(8, { timeout: 8_000 })

    await checkpoint(page, 'AR-04-airia-tools-list')
  })

  test('AR-05 — F1 theme badge visible on Race Control', async ({ page }) => {
    await page.goto('/race-control')
    await expect(page.getByTestId('race-control-page')).toBeVisible({ timeout: 10_000 })

    const badge = page.getByTestId('f1-theme-badge')
    await expect(badge).toBeVisible({ timeout: 5_000 })
    const text = await badge.textContent()
    expect(text).toContain('Race Beyond the Track')

    await checkpoint(page, 'AR-05-f1-theme-badge')
  })

  test('AR-06 — nav link reaches /airia page', async ({ page }) => {
    await page.goto('/')
    const link = page.getByTestId('nav-airia')
    await expect(link).toBeVisible({ timeout: 5_000 })
    await link.click()
    await expect(page.getByTestId('airia-readiness-page')).toBeVisible({ timeout: 8_000 })
    await checkpoint(page, 'AR-06-nav-airia')
  })

  test('AR-07 — API /api/airia/status returns PASS', async ({ page }) => {
    const resp = await page.request.get(`${API}/api/airia/status`)
    expect(resp.status()).toBe(200)
    const data = await resp.json()
    expect(data.validator_status).toBe('PASS')
    expect(data.bundle_hash.length).toBeGreaterThan(10)
    expect(data.tools.length).toBeGreaterThanOrEqual(8)
  })

  test('AR-08 — bundle path element visible on /airia', async ({ page }) => {
    await page.goto('/airia')
    await expect(page.getByTestId('airia-readiness-page')).toBeVisible({ timeout: 10_000 })

    const pathEl = page.getByTestId('airia-bundle-path')
    await expect(pathEl).toBeVisible({ timeout: 8_000 })
    const text = await pathEl.textContent()
    expect(text).toContain('artifacts/airia')

    await checkpoint(page, 'AR-08-bundle-path')
  })
})
