// ZY-HR 前端页面截图工具 — 用于重构验证
const { chromium } = require('playwright');

(async () => {
  const url = process.argv[2];
  const output = process.argv[3] || '/tmp/screenshot.png';
  if (!url) { console.error('用法: node screenshot.js <URL> [输出路径]'); process.exit(1); }

  const browser = await chromium.launch({
    headless: true,
    proxy: { server: 'http://127.0.0.1:7897' }
  });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(1000);
  await page.screenshot({ path: output, fullPage: false });
  await browser.close();
  console.log(`✅ 截图已保存: ${output}`);
})();
