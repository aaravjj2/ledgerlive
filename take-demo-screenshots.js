// Playwright screenshot script for LedgerLive hackathon demo
// Run with: node take-demo-screenshots.js

const { chromium } = require('/home/aarav/Aarav/ledgerlive/ledgerlive/apps/web/node_modules/playwright-core');
const path = require('path');
const fs = require('fs');

const BASE_URL = 'https://ledgerlive-web-zkw2sk4rha-uc.a.run.app';
const OUTPUT_DIR = '/home/aarav/Aarav/ledgerlive/ledgerlive/artifacts/demo';

const PAGES = [
  {
    id: '01-dashboard',
    url: `${BASE_URL}/`,
    filename: '01-dashboard.png',
  },
  {
    id: '02-race-control',
    url: `${BASE_URL}/race-control`,
    filename: '02-race-control.png',
  },
  {
    id: '03-documents',
    url: `${BASE_URL}/documents`,
    filename: '03-documents.png',
  },
  {
    id: '04-reconciliation',
    url: `${BASE_URL}/reconciliation`,
    filename: '04-reconciliation.png',
  },
  {
    id: '05-exceptions',
    url: `${BASE_URL}/exceptions`,
    filename: '05-exceptions.png',
  },
  {
    id: '06-review',
    url: `${BASE_URL}/review`,
    filename: '06-review.png',
  },
  {
    id: '07-audit',
    url: `${BASE_URL}/audit`,
    filename: '07-audit.png',
  },
  {
    id: '08-voice',
    url: `${BASE_URL}/live-voice`,
    filename: '08-voice.png',
  },
];

async function takeScreenshots() {
  // Ensure output directory exists
  if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  }

  const browser = await chromium.launch({
    headless: false,
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });

  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 },
  });

  const page = await context.newPage();
  const results = [];

  // First, warm up: navigate to base URL and wait for network idle
  console.log(`[WARM-UP] Navigating to ${BASE_URL}/`);
  try {
    await page.goto(`${BASE_URL}/`, { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(2000);
    console.log('[WARM-UP] Base URL loaded successfully');
  } catch (err) {
    console.error('[WARM-UP] Warning:', err.message);
  }

  for (const pageConfig of PAGES) {
    console.log(`\n[SCREENSHOT] ${pageConfig.id} -> ${pageConfig.url}`);
    const outputPath = path.join(OUTPUT_DIR, pageConfig.filename);

    try {
      await page.goto(pageConfig.url, { waitUntil: 'networkidle', timeout: 30000 });
      await page.waitForTimeout(2000);

      // Capture full-page screenshot
      await page.screenshot({
        path: outputPath,
        fullPage: true,
      });

      // Get page title and any visible text for status reporting
      const title = await page.title();
      const bodyText = await page.evaluate(() => {
        const body = document.body;
        return body ? body.innerText.substring(0, 500) : '';
      });

      // Check for common error indicators
      const has404 = bodyText.includes('404') || bodyText.includes('not found') || bodyText.includes('Page Not Found');
      const hasError = bodyText.includes('Error') || bodyText.includes('error') || bodyText.includes('BROKEN');
      const isEmpty = bodyText.trim().length < 50;

      let status = 'LOOKS GOOD';
      if (has404) status = 'BROKEN (404/Not Found)';
      else if (hasError) status = 'BROKEN (Error)';
      else if (isEmpty) status = 'EMPTY STATE';

      results.push({
        id: pageConfig.id,
        status,
        title,
        snippet: bodyText.substring(0, 200).replace(/\n/g, ' ').trim(),
        saved: outputPath,
      });

      console.log(`  Status: ${status}`);
      console.log(`  Title: ${title}`);
      console.log(`  Saved: ${outputPath}`);
    } catch (err) {
      results.push({
        id: pageConfig.id,
        status: 'BROKEN (Navigation Error)',
        error: err.message,
        saved: null,
      });
      console.error(`  ERROR: ${err.message}`);
    }
  }

  await browser.close();

  // Write report
  const reportPath = path.join(OUTPUT_DIR, 'report.json');
  fs.writeFileSync(reportPath, JSON.stringify(results, null, 2));

  console.log('\n\n=== PAGE RESULTS ===');
  for (const r of results) {
    console.log(`${r.id}: [${r.status}] - ${r.snippet || r.error || 'No details'}`);
  }
  console.log(`\nReport saved to: ${reportPath}`);
}

takeScreenshots().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
