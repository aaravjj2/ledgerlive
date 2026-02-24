/**
 * channel-actions.spec.ts
 *
 * CHANNEL APPROVAL — Verify golden scenario channel send-approval action.
 * Sends approval via mock channel, verifies trace_id in response, and
 * checks audit log updates.
 *
 * SELECTOR POLICY: data-testid ONLY.
 */
import { test, expect } from '@playwright/test'
import { initE2E, checkpoint, gotoPage } from './helpers'

const API = 'http://127.0.0.1:8090'

test.describe('Channel Actions', () => {
  test.beforeEach(async ({ page }) => {
    await initE2E(page)
    // Seed golden state before each test
    await page.request.post(`${API}/api/ops/golden-scenario-run`)
  })

  test('CHAN-01 — send-approval returns trace_id and channel_action_id', async ({ page }) => {
    const resp = await page.request.post(`${API}/api/ops/channel/send-approval`, {
      data: { message: 'golden-e2e approval' },
    })
    expect(resp.ok()).toBeTruthy()
    const json = await resp.json()

    expect(json.channel_action_id).toBeTruthy()
    expect(json.channel_action_id).toContain('grc-')
    expect(json.trace_id).toBeTruthy()
    expect(json.status).toBeTruthy()
    await checkpoint(page, 'chan-01-send-approval')
  })

  test('CHAN-02 — trace_id is a non-empty string', async ({ page }) => {
    const resp = await page.request.post(`${API}/api/ops/channel/send-approval`)
    const json = await resp.json()

    expect(typeof json.trace_id).toBe('string')
    expect(json.trace_id.length).toBeGreaterThan(0)
    await checkpoint(page, 'chan-02-trace-id')
  })

  test('CHAN-03 — audit log page loads after channel action', async ({ page }) => {
    // Trigger channel action
    await page.request.post(`${API}/api/ops/channel/send-approval`)

    // Navigate to audit log and verify it loads
    await gotoPage(page, '/audit', 'audit-page')
    await expect(page.getByTestId('audit-page')).toBeVisible()
    await checkpoint(page, 'chan-03-audit-after-channel')
  })

  test('CHAN-04 — repeated sends return consistent golden channel_action_id', async ({ page }) => {
    const resp1 = await page.request.post(`${API}/api/ops/channel/send-approval`)
    const j1 = await resp1.json()
    const resp2 = await page.request.post(`${API}/api/ops/channel/send-approval`)
    const j2 = await resp2.json()

    // Both should reference the same deterministic golden channel action ID
    expect(j1.channel_action_id).toBe(j2.channel_action_id)
    await checkpoint(page, 'chan-04-deterministic-id')
  })
})
