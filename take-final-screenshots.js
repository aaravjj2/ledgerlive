// Take FINAL screenshots of all P0 pages after redesign
const { chromium } = require('/home/aarav/Aarav/ledgerlive/ledgerlive/apps/web/node_modules/playwright-core');
const path = require('path');
const fs = require('fs');

const BASE = 'http://localhost:5173';
const OUT = '/home/aarav/Aarav/ledgerlive/ledgerlive/artifacts/demo';

const PAGES = [
  { name: 'FINAL-01-dashboard',          url: '/' },
  { name: 'FINAL-02-race-control',       url: '/race-control' },
  { name: 'FINAL-03-cfo-cockpit',        url: '/cfo-cockpit' },
  { name: 'FINAL-04-evidence-binder',    url: '/evidence-binder' },
  { name: 'FINAL-05-multi-agent',        url: '/multi-agent' },
  { name: 'FINAL-06-close-calendar',     url: '/close-calendar' },
  { name: 'FINAL-07-audit-log',          url: '/audit' },
  { name: 'FINAL-08-board-pack',         url: '/board-pack' },
  { name: 'FINAL-09-gradient-ai',        url: '/gradient-ai' },
  { name: 'FINAL-10-connectors',         url: '/connectors' },
  { name: 'FINAL-11-bloomberg',          url: '/bloomberg' },
  { name: 'FINAL-12-hackathon',          url: '/hackathon-showcase' },
  { name: 'FINAL-13-exceptions',         url: '/exceptions' },
  { name: 'FINAL-14-documents',          url: '/documents' },
  { name: 'FINAL-15-live-voice',         url: '/live-voice' },
];

async function main() {
  if (!fs.existsSync(OUT)) fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({ headless: false });
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await ctx.newPage();

  const results = [];
  for (const p of PAGES) {
    try {
      await page.goto(BASE + p.url, { waitUntil: 'networkidle', timeout: 15000 });
      await page.waitForTimeout(1500);
      const fp = path.join(OUT, p.name + '.png');
      await page.screenshot({ path: fp, fullPage: false });
      const size = Math.round(fs.statSync(fp).size / 1024);
      console.log(`✓ ${p.name}.png (${size}KB)`);
      results.push({ name: p.name, size, status: 'OK' });
    } catch (e) {
      console.log(`✗ ${p.name} — ${e.message}`);
      results.push({ name: p.name, status: 'FAIL', error: e.message });
    }
  }

  await browser.close();
  console.log('\n=== SUMMARY ===');
  const passed = results.filter(r => r.status === 'OK').length;
  console.log(`${passed}/${results.length} screenshots captured`);
  results.filter(r => r.status === 'FAIL').forEach(r => console.log(`  FAIL: ${r.name} — ${r.error}`));
}

main().catch(e => { console.error(e); process.exit(1); });
