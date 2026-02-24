/**
 * security-blocks.spec.ts
 *
 * SECURITY EVENTS — Verify golden scenario seeds a blocked security event,
 * and that the Fix Path action resolves it.
 *
 * SELECTOR POLICY: data-testid ONLY.
 */
import { test, expect } from '@playwright/test'
import { initE2E, checkpoint } from './helpers'

const API = 'http://127.0.0.1:8090'

test.describe('Security Blocks', () => {
  test.beforeEach(async ({ page }) => {
    await initE2E(page)
  })

  test('SEC-01 — golden seed produces a BLOCKED event visible in RC', async ({ page }) => {
    // Seed via API directly so we can control timing
    const seedResp = await page.request.post(`${API}/api/ops/golden-scenario-run`)
    expect(seedResp.ok()).toBeTruthy()
    const seedJson = await seedResp.json()
    expect(seedJson.status).toBe('seeded')

    // Navigate to Race Control and reload (security-events included in loadAll)
    await page.goto('/race-control')
    await expect(page.getByTestId('race-control-page')).toBeVisible({ timeout: 10_000 })

    // The security events section should appear automatically since securityEvents.length > 0
    await expect(page.getByTestId('rc-security-events-section')).toBeVisible({ timeout: 10_000 })
    await expect(page.getByTestId('rc-security-event-card')).toBeVisible()

    // Card text should indicate BLOCKED
    const cardText = await page.getByTestId('rc-security-event-card').innerText()
    expect(cardText).toContain('BLOCKED')
    await checkpoint(page, 'sec-01-blocked-event')
  })

  test('SEC-02 — Fix Path resolves the blocked event', async ({ page }) => {
    // Seed state
    await page.request.post(`${API}/api/ops/golden-scenario-run`)

    await page.goto('/race-control')
    await expect(page.getByTestId('rc-security-events-section')).toBeVisible({ timeout: 10_000 })

    // Should have a fix button (fix not yet applied)
    const fixBtn = page.locator('[data-testid^="rc-security-fix-"]').first()
    await expect(fixBtn).toBeVisible({ timeout: 5_000 })
    await checkpoint(page, 'sec-02-before-fix')

    await fixBtn.click()

    // After fix, fixed badge should appear and fix button should disappear
    await expect(page.locator('[data-testid^="rc-security-fixed-badge-"]').first()).toBeVisible({ timeout: 10_000 })
    await expect(fixBtn).not.toBeVisible({ timeout: 5_000 })
    await checkpoint(page, 'sec-02-fixed')
  })

  test('SEC-03 — security-event API returns correct golden data', async ({ page }) => {
    await page.request.post(`${API}/api/ops/golden-scenario-run`)

    const listResp = await page.request.get(`${API}/api/ops/security-events`)
    expect(listResp.ok()).toBeTruthy()
    const list = await listResp.json()
    expect(list.items).toBeDefined()
    expect(list.items.length).toBeGreaterThanOrEqual(1)

    const evt = list.items[0]
    expect(evt.blocked).toBe(true)
    expect(evt.event_id).toContain('grc-')
    await checkpoint(page, 'sec-03-api-verify')
  })

  test('SEC-04 — fix-path API marks event as resolved', async ({ page }) => {
    await page.request.post(`${API}/api/ops/golden-scenario-run`)

    const listResp = await page.request.get(`${API}/api/ops/security-events`)
    const list = await listResp.json()
    const eventId = list.items[0].event_id

    // Apply fix via API
    const fixResp = await page.request.post(`${API}/api/ops/security-event/${eventId}/fix-path`)
    expect(fixResp.ok()).toBeTruthy()
    const fixJson = await fixResp.json()
    expect(fixJson.fix_applied).toBe(true)

    // Re-fetch and verify
    const recheck = await (await page.request.get(`${API}/api/ops/security-event/${eventId}`)).json()
    expect(recheck.fix_applied).toBe(true)
    await checkpoint(page, 'sec-04-api-fix-resolved')
  })
})
