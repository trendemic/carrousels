const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const dir = process.argv[2], name = process.argv[3];
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  await p.goto('file://' + path.join(dir, 'carrousel.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(400);
  const pages = await p.$$('section.page');
  for (let i = 0; i < pages.length; i++) await pages[i].screenshot({ path: path.join(dir, `slide-${i + 1}.png`) });
  await p.addStyleTag({ content: '@page{size:1080px 1350px;margin:0}body{background:none}.page{break-after:page}' });
  await p.pdf({ path: path.join(dir, name + '.pdf'), width: '1080px', height: '1350px', printBackground: true });
  await b.close();
})();
