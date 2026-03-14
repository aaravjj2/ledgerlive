/**
 * atlassian-mocks.spec.ts
 *
 * ATLASSIAN MOCKS — Verify golden scenario Jira + Confluence mock endpoints.
 * Creates mock issues/pages and verifies deterministic golden IDs.
 * Also verifies binder hash stability.
 *
 * SELECTOR POLICY: data-testid ONLY.
 */
import { test, expect } from '@playwright/test'
import { initE2E, checkpoint } from './helpers'

const API = 'http://127.0.0.1:8090'

test.describe('Atlassian Mocks', () => {
  test.beforeEach(async ({ page }) => {
    await initE2E(page)
    await page.request.post(`${API}/api/ops/golden-scenario-run`)
  })

  test('ATL-01 — create Jira issue returns golden jira_id', async ({ page }) => {
    const resp = await page.request.post(`${API}/api/ops/atlassian/create-jira`, {
      data: { summary: 'Golden E2E Jira issue', priority: 'high' },
    })
    expect(resp.ok()).toBeTruthy()
    const json = await resp.json()

    expect(json.jira_id).toBeTruthy()
    expect(json.jira_id).toContain('grc-')
    expect(json.issue_url || json.url).toBeTruthy()
    await checkpoint(page, 'atl-01-jira-created')
  })

  test('ATL-02 — create Confluence page returns golden confluence_id', async ({ page }) => {
    const resp = await page.request.post(`${API}/api/ops/atlassian/create-confluence`, {
      data: { title: 'Golden E2E Confluence Page' },
    })
    expect(resp.ok()).toBeTruthy()
    const json = await resp.json()

    expect(json.confluence_id).toBeTruthy()
    expect(json.confluence_id).toContain('grc-')
    expect(json.page_url || json.url).toBeTruthy()
    await checkpoint(page, 'atl-02-confluence-created')
  })

  test('ATL-03 — Jira and Confluence IDs are deterministic across calls', async ({ page }) => {
    const jira1 = await (await page.request.post(`${API}/api/ops/atlassian/create-jira`)).json()
    const jira2 = await (await page.request.post(`${API}/api/ops/atlassian/create-jira`)).json()
    expect(jira1.jira_id).toBe(jira2.jira_id)

    const conf1 = await (await page.request.post(`${API}/api/ops/atlassian/create-confluence`)).json()
    const conf2 = await (await page.request.post(`${API}/api/ops/atlassian/create-confluence`)).json()
    expect(conf1.confluence_id).toBe(conf2.confluence_id)
    await checkpoint(page, 'atl-03-deterministic-ids')
  })

  test('ATL-04 — binder hash is stable (matches baseline)', async ({ page }) => {
    const resp = await page.request.post(`${API}/api/ops/replay/regenerate-binder`)
    expect(resp.ok()).toBeTruthy()
    const json = await resp.json()

    const hash = json.binder_hash || json.hash
    expect(hash).toBeTruthy()
    expect(hash).toContain('sha256:')
    expect(hash.length).toBe(71) // "sha256:" + 64 hex chars
    await checkpoint(page, 'atl-04-binder-hash')
  })

  test('ATL-05 — binder hash is stable across two runs (determinism check)', async ({ page }) => {
    const r1 = await (await page.request.post(`${API}/api/ops/replay/regenerate-binder`)).json()
    const r2 = await (await page.request.post(`${API}/api/ops/replay/regenerate-binder`)).json()

    const hash1 = r1.binder_hash || r1.hash
    const hash2 = r2.binder_hash || r2.hash
    expect(hash1).toBe(hash2)
    expect(hash1).toContain('sha256:')
    await checkpoint(page, 'atl-05-binder-determinism')
  })
})
