import { defineConfig, devices } from '@playwright/test'
import * as path from 'path'

// Set absolute screenshots dir for checkpoint() helper before workers spawn
process.env.PLAYWRIGHT_SCREENSHOTS_DIR = path.resolve(process.cwd(), 'test-results', 'screenshots')

/**
 * LedgerLive — Strict MCP headed-only Playwright configuration.
 *
 * HARD REQUIREMENTS:
 * - headless: false (headed mode only)
 * - retries: 0, workers: 1
 * - video: on, trace: on, screenshot: on
 * - Only data-testid selectors
 * - baseURL: vite preview at 127.0.0.1:4173
 */

if (process.env.PLAYWRIGHT_HEADLESS === 'true' || process.env.HEADLESS === 'true') {
  throw new Error('FATAL: Headed-only mode enforced. PLAYWRIGHT_HEADLESS / HEADLESS=true is FORBIDDEN.')
}

export default defineConfig({
  testDir: './e2e',
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: 0,
  workers: 1,
  reporter: [
    ['list'],
    ['html', { outputFolder: 'playwright-report', open: 'never' }],
    ['json', { outputFile: 'test-results/results.json' }],
  ],
  outputDir: 'test-results',
  use: {
    headless: false,
    baseURL: process.env.PLAYWRIGHT_BASE_URL ?? 'http://127.0.0.1:4173',
    trace: 'on',
    screenshot: 'on',
    video: 'on',
    actionTimeout: 15_000,
    navigationTimeout: 20_000,
    testIdAttribute: 'data-testid',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'], headless: false },
    },
  ],
  webServer: {
    command: 'npx vite build && npx vite preview --host 127.0.0.1 --port 4173',
    url: 'http://127.0.0.1:4173',
    reuseExistingServer: !process.env.CI,
    timeout: 120_000,
  },
})
