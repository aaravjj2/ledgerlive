/**
 * race-weekend-timeline.spec.ts
 *
 * Race Weekend Timeline — E2E walkthrough of the Race Control page timeline.
 * Validates: timeline renders with 6 stage cards, lap time tiles present,
 * stage labels match canonical order, safety car logic correct.
 *
 * SELECTOR POLICY: data-testid ONLY.
 */
import { test, expect } from '@playwright/test'
import { checkpoint } from './helpers'

test.describe('Race Weekend Timeline', () => {
  test('RWT-01 — /race-control renders Race Weekend Timeline section', async ({ page }) => {
    await page.goto('/race-control')
    await expect(page.getByTestId('race-control-page')).toBeVisible({ timeout: 10_000 })

    const timeline = page.getByTestId('rc-race-weekend-timeline')
    await expect(timeline).toBeVisible({ timeout: 10_000 })

    await checkpoint(page, 'RWT-01-timeline-visible')
  })

  test('RWT-02 — timeline has exactly 6 stage cards', async ({ page }) => {
    await page.goto('/race-control')
    await expect(page.getByTestId('race-control-page')).toBeVisible({ timeout: 10_000 })

    const timeline = page.getByTestId('rc-race-weekend-timeline')
    await expect(timeline).toBeVisible({ timeout: 10_000 })

    const cards = page.getByTestId('rc-stage-card')
    await expect(cards).toHaveCount(6, { timeout: 8_000 })

    await checkpoint(page, 'RWT-02-six-stage-cards')
  })

  test('RWT-03 — stage cards show canonical labels', async ({ page }) => {
    await page.goto('/race-control')
    await expect(page.getByTestId('race-control-page')).toBeVisible({ timeout: 10_000 })

    const timeline = page.getByTestId('rc-race-weekend-timeline')
    await expect(timeline).toBeVisible({ timeout: 10_000 })

    const cards = page.getByTestId('rc-stage-card')
    await expect(cards).toHaveCount(6, { timeout: 8_000 })

    // Check canonical labels present in the timeline
    const timelineText = await timeline.textContent()
    expect(timelineText).toContain('Qualifying')
    expect(timelineText).toContain('Formation Lap')
    expect(timelineText).toContain('Pit Stop 1')
    expect(timelineText).toContain('Safety Car')
    expect(timelineText).toContain('Pit Stop 2')
    expect(timelineText).toContain('Checkered Flag')

    await checkpoint(page, 'RWT-03-stage-labels')
  })

  test('RWT-04 — lap time tiles visible on completed stages', async ({ page }) => {
    await page.goto('/race-control')
    await expect(page.getByTestId('race-control-page')).toBeVisible({ timeout: 10_000 })

    const timeline = page.getByTestId('rc-race-weekend-timeline')
    await expect(timeline).toBeVisible({ timeout: 10_000 })

    // At least one lap time tile should be visible (from completed stages)
    const lapTiles = page.getByTestId('rc-lap-time-tile')
    const count = await lapTiles.count()
    expect(count).toBeGreaterThanOrEqual(1)

    await checkpoint(page, 'RWT-04-lap-time-tiles')
  })

  test('RWT-05 — Safety Car stage card has approval and fail-closed badges', async ({ page }) => {
    await page.goto('/race-control')
    await expect(page.getByTestId('race-control-page')).toBeVisible({ timeout: 10_000 })

    const timeline = page.getByTestId('rc-race-weekend-timeline')
    await expect(timeline).toBeVisible({ timeout: 10_000 })

    // Find safety car card by looking for its badge content
    const timelineText = await timeline.textContent()
    expect(timelineText).toContain('fail-closed')
    expect(timelineText).toContain('approval')

    await checkpoint(page, 'RWT-05-safety-car-badges')
  })

  test('RWT-06 — timeline API endpoint returns all 6 stages', async ({ page }) => {
    const resp = await page.request.get('http://127.0.0.1:8090/api/race-weekend/stages')
    expect(resp.status()).toBe(200)
    const data = await resp.json()
    expect(data.stages).toHaveLength(6)
    expect(data.safety_car_active).toBeDefined()
    expect(data.critical_path).toHaveLength(6)
    expect(data.critical_path[0]).toBe('qualifying')
    expect(data.critical_path[5]).toBe('checkered_flag')
  })

  test('RWT-07 — stage order is deterministic on two calls', async ({ page }) => {
    const r1 = await page.request.get('http://127.0.0.1:8090/api/race-weekend/stages')
    const r2 = await page.request.get('http://127.0.0.1:8090/api/race-weekend/stages')
    const d1 = await r1.json()
    const d2 = await r2.json()
    const keys1 = d1.stages.map((s: { key: string }) => s.key)
    const keys2 = d2.stages.map((s: { key: string }) => s.key)
    expect(keys1).toEqual(keys2)
    expect(d1.critical_path).toEqual(d2.critical_path)
  })

  test('RWT-08 — Race Control run golden shows timeline non-empty stages', async ({ page }) => {
    await page.goto('/race-control')
    await expect(page.getByTestId('race-control-page')).toBeVisible({ timeout: 10_000 })

    // Click Run Canonical
    await page.getByTestId('race-control-run-golden').click()
    await expect(page.getByTestId('rc-run-status')).toBeVisible({ timeout: 15_000 })

    // Timeline still visible after seed
    const timeline = page.getByTestId('rc-race-weekend-timeline')
    await expect(timeline).toBeVisible({ timeout: 8_000 })

    const cards = page.getByTestId('rc-stage-card')
    const count = await cards.count()
    expect(count).toBe(6)

    await checkpoint(page, 'RWT-08-timeline-after-golden')
  })
})
