/**
 * golden-race-control.spec.ts
 *
 * GOLDEN SCENARIO — Full Race Control E2E walkthrough.
 * Seeds deterministic state, verifies every major RC panel,
 * exercises Why/Verify/Approve inline actions, export packs, and replay.
 *
 * SELECTOR POLICY: data-testid ONLY.
 */
import { test, expect } from '@playwright/test'
import { initE2E, seedGolden, checkpoint, getAssertions } from './helpers'

test.describe('Golden Race Control', () => {
  test.beforeEach(async ({ page }) => {
    await initE2E(page)
  })

  test('RC-01 — seed golden scenario and verify panels load', async ({ page }) => {
    // Navigate to Race Control
    await page.goto('/race-control')
    await expect(page.getByTestId('race-control-page')).toBeVisible({ timeout: 10_000 })

    // Click Run Canonical — seeds all golden data
    await page.getByTestId('race-control-run-golden').click()
    await expect(page.getByTestId('rc-run-status')).toHaveText('SEEDED', { timeout: 15_000 })
    await checkpoint(page, 'rc-01-seeded')

    // Verify assertions match golden counts
    const assertions = await getAssertions(page)
    expect(assertions['lanes']).toBe(2)
    expect(assertions['checkpoints']).toBe(3)
    expect(assertions['incidents']).toBe(1)
    expect(assertions['approval_steps']).toBe(2)
    expect(assertions['security_events']).toBe(1)
    await checkpoint(page, 'rc-01-assertions')
  })

  test('RC-02 — lane cards are rendered after seed', async ({ page }) => {
    await page.goto('/race-control')
    await expect(page.getByTestId('race-control-page')).toBeVisible()
    await page.getByTestId('race-control-run-golden').click()
    await expect(page.getByTestId('rc-run-status')).toBeVisible({ timeout: 15_000 })

    // 2 lane cards
    const laneCards = page.getByTestId('rc-lane-card')
    await expect(laneCards).toHaveCount(2, { timeout: 10_000 })
    await checkpoint(page, 'rc-02-lanes')
  })

  test('RC-03 — checkpoint rows and Why/Verify dossier', async ({ page }) => {
    await page.goto('/race-control')
    await expect(page.getByTestId('race-control-page')).toBeVisible()
    await page.getByTestId('race-control-run-golden').click()
    await expect(page.getByTestId('rc-run-status')).toBeVisible({ timeout: 15_000 })

    // 3 checkpoint rows
    const rows = page.getByTestId('rc-checkpoint-row')
    await expect(rows).toHaveCount(3, { timeout: 10_000 })

    // Click Why on first checkpoint
    await page.getByTestId('rc-checkpoint-why-0').click()
    await expect(page.getByTestId('rc-dossier-modal')).toBeVisible({ timeout: 5_000 })
    await expect(page.getByTestId('rc-dossier-content')).not.toBeEmpty()
    await checkpoint(page, 'rc-03-why-dossier')
    await page.getByTestId('rc-dossier-close').click()
    await expect(page.getByTestId('rc-dossier-modal')).not.toBeVisible()

    // Click Verify on first checkpoint
    await page.getByTestId('rc-checkpoint-verify-0').click()
    await expect(page.getByTestId('rc-dossier-modal')).toBeVisible({ timeout: 5_000 })
    await checkpoint(page, 'rc-03-verify-dossier')
    await page.getByTestId('rc-dossier-close').click()
  })

  test('RC-04 — incident log and Why dossier', async ({ page }) => {
    await page.goto('/race-control')
    await expect(page.getByTestId('race-control-page')).toBeVisible()
    await page.getByTestId('race-control-run-golden').click()
    await expect(page.getByTestId('rc-run-status')).toBeVisible({ timeout: 15_000 })

    // 1 incident card
    await expect(page.getByTestId('rc-incident-card')).toHaveCount(1, { timeout: 10_000 })

    // Click Why on incident 0
    await page.getByTestId('rc-incident-why-0').click()
    await expect(page.getByTestId('rc-dossier-modal')).toBeVisible({ timeout: 5_000 })
    await expect(page.getByTestId('rc-dossier-content')).not.toBeEmpty()
    await checkpoint(page, 'rc-04-incident-why')
    await page.getByTestId('rc-dossier-close').click()
  })

  test('RC-05 — approval chain and approve pending step', async ({ page }) => {
    await page.goto('/race-control')
    await expect(page.getByTestId('race-control-page')).toBeVisible()
    await page.getByTestId('race-control-run-golden').click()
    await expect(page.getByTestId('rc-run-status')).toBeVisible({ timeout: 15_000 })

    // 2 approval rows
    await expect(page.getByTestId('rc-approval-row')).toHaveCount(2, { timeout: 10_000 })

    // There should be exactly one pending Approve button
    const approveBtn = page.locator('[data-testid^="rc-approval-approve-"]').first()
    await expect(approveBtn).toBeVisible({ timeout: 5_000 })
    await checkpoint(page, 'rc-05-before-approve')
    await approveBtn.click()

    // After approval the button should disappear (step is now approved)
    await expect(approveBtn).not.toBeVisible({ timeout: 10_000 })
    await checkpoint(page, 'rc-05-after-approve')
  })

  test('RC-06 — export telemetry and court packs', async ({ page }) => {
    await page.goto('/race-control')
    await expect(page.getByTestId('race-control-page')).toBeVisible()
    await page.getByTestId('race-control-run-golden').click()
    await expect(page.getByTestId('rc-run-status')).toBeVisible({ timeout: 15_000 })

    // Export telemetry
    await page.getByTestId('rc-export-telemetry').click()
    await expect(page.getByTestId('rc-export-telemetry-badge')).toBeVisible({ timeout: 10_000 })
    const telemBadge = await page.getByTestId('rc-export-telemetry-badge').innerText()
    expect(['PASS', 'OK', 'seeded'].some(v => telemBadge.toUpperCase().includes(v.toUpperCase()))).toBeTruthy()
    await checkpoint(page, 'rc-06-telem-badge')

    // Export court pack
    await page.getByTestId('rc-export-court').click()
    await expect(page.getByTestId('rc-export-court-badge')).toBeVisible({ timeout: 10_000 })
    const courtBadge = await page.getByTestId('rc-export-court-badge').innerText()
    expect(courtBadge.length).toBeGreaterThan(0)
    await checkpoint(page, 'rc-06-court-badge')
  })

  test('RC-07 — replay viewer and binder hash', async ({ page }) => {
    await page.goto('/race-control')
    await expect(page.getByTestId('race-control-page')).toBeVisible()
    await page.getByTestId('race-control-run-golden').click()
    await expect(page.getByTestId('rc-run-status')).toBeVisible({ timeout: 15_000 })

    // Open replay
    await page.getByTestId('rc-replay-open').click()
    await expect(page.getByTestId('rc-replay-regen')).toBeVisible({ timeout: 5_000 })

    // Regenerate binder
    await page.getByTestId('rc-replay-regen').click()
    await expect(page.getByTestId('rc-replay-hash-badge')).toBeVisible({ timeout: 10_000 })
    const hash = await page.getByTestId('rc-replay-hash-badge').getAttribute('title')
    expect(hash).toBeTruthy()
    expect(hash).toContain('sha256:')
    await checkpoint(page, 'rc-07-replay-hash')
  })
})
