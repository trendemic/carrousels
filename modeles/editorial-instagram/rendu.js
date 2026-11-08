const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const dir = __dirname;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1350 } });
  await page.goto('file://' + path.join(dir, 'carrousel.html'));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(500);
  const slides = await page.$$('section.page');
  for (let i = 0; i < slides.length; i++) {
    await slides[i].screenshot({ path: path.join(dir, `slide-${i + 1}.png`) });
  }
  await browser.close();
})();
