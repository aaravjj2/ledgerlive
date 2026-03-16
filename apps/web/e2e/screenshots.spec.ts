import { test } from '@playwright/test';

const baseUrl = 'http://localhost:5173';
const pages = [
  { url: '/forecasting', file: 'POLISH3-01-forecasting.png' },
  { url: '/budgeting', file: 'POLISH3-02-budgeting.png' },
  { url: '/financial-statements', file: 'POLISH3-03-financials.png' },
  { url: '/consolidation', file: 'POLISH3-04-consolidation.png' },
  { url: '/controls', file: 'POLISH3-05-controls.png' },
  { url: '/soc2', file: 'POLISH3-06-soc2.png' },
  { url: '/trace-explorer', file: 'POLISH3-07-trace.png' },
  { url: '/agent-runtime', file: 'POLISH3-08-agent-runtime.png' },
  { url: '/readiness-dashboard', file: 'POLISH3-09-readiness.png' },
  { url: '/lap-time-telemetry', file: 'POLISH3-10-lap-telemetry.png' },
  { url: '/audit', file: 'POLISH3-11-audit.png' },
  { url: '/close-calendar', file: 'POLISH3-12-calendar.png' },
  { url: '/settings', file: 'POLISH3-13-settings.png' },
  { url: '/connectors', file: 'POLISH3-14-connectors.png' },
];

pages.forEach(({ url, file }) => {
  test(`screenshot ${file}`, async ({ page }) => {
    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto(`${baseUrl}${url}`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(500);
    await page.screenshot({ path: `../../../artifacts/demo/${file}`, fullPage: false });
  });
});
