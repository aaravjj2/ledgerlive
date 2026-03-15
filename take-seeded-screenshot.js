// Take final seeded dashboard screenshot
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

  // Dashboard seeded
  await page.goto(BASE_URL, { waitUntil: 'networkidle' });
  await page.waitForTimeout(3000);
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'NEW-03-dashboard-seeded.png'), fullPage: false });
  console.log('NEW-03-dashboard-seeded.png saved');

  // Race control with seeded data
  await page.goto(BASE_URL + '/race-control', { waitUntil: 'networkidle' });
  await page.waitForTimeout(3000);
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'NEW-08-race-control-seeded.png'), fullPage: false });
  console.log('NEW-08-race-control-seeded.png saved');

  // Exceptions with seeded data
  await page.goto(BASE_URL + '/exceptions', { waitUntil: 'networkidle' });
  await page.waitForTimeout(2000);
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'NEW-09-exceptions-seeded.png'), fullPage: false });
  console.log('NEW-09-exceptions-seeded.png saved');

  await browser.close();
  console.log('\nSeeded screenshots saved to:', OUTPUT_DIR);
}

main().catch(e => { console.error(e); process.exit(1); });
