// Screenshot script for new LedgerLive UI
const { chromium } = require('/home/aarav/Aarav/ledgerlive/ledgerlive/apps/web/node_modules/playwright-core');
const path = require('path');
const fs = require('fs');

const BASE_URL = 'http://localhost:5173';
const OUTPUT_DIR = '/home/aarav/Aarav/ledgerlive/ledgerlive/artifacts/demo';

async function main() {
  if (!fs.existsSync(OUTPUT_DIR)) fs.mkdirSync(OUTPUT_DIR, { recursive: true });

  const browser = await chromium.launch({ headless: false });
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await ctx.newPage();

  // First load to let React hydrate
  await page.goto(BASE_URL, { waitUntil: 'networkidle' });
  await page.waitForTimeout(2000);
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'NEW-01-dashboard.png'), fullPage: false });
  console.log('NEW-01-dashboard.png saved');

  // Race control
  await page.goto(BASE_URL + '/race-control', { waitUntil: 'networkidle' });
  await page.waitForTimeout(2000);
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'NEW-02-race-control.png'), fullPage: false });
  console.log('NEW-02-race-control.png saved');

  // Exceptions
  await page.goto(BASE_URL + '/exceptions', { waitUntil: 'networkidle' });
  await page.waitForTimeout(1500);
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'NEW-03-exceptions.png'), fullPage: false });
  console.log('NEW-03-exceptions.png saved');

  // Reconciliation
  await page.goto(BASE_URL + '/reconciliation', { waitUntil: 'networkidle' });
  await page.waitForTimeout(1500);
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'NEW-04-reconciliation.png'), fullPage: false });
  console.log('NEW-04-reconciliation.png saved');

  // Live voice
  await page.goto(BASE_URL + '/live-voice', { waitUntil: 'networkidle' });
  await page.waitForTimeout(1500);
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'NEW-05-live-voice.png'), fullPage: false });
  console.log('NEW-05-live-voice.png saved');

  // Audit log
  await page.goto(BASE_URL + '/audit', { waitUntil: 'networkidle' });
  await page.waitForTimeout(1500);
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'NEW-06-audit.png'), fullPage: false });
  console.log('NEW-06-audit.png saved');

  // Navigate back to dashboard and show sidebar open
  await page.goto(BASE_URL, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1500);
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'NEW-07-sidebar.png'), fullPage: false });
  console.log('NEW-07-sidebar.png saved');

  await browser.close();
  console.log('\nAll screenshots saved to:', OUTPUT_DIR);
}

main().catch(e => { console.error(e); process.exit(1); });
