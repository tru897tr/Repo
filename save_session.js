// save_session.js
const fs = require('fs');
const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({ headless: false, args: ['--no-sandbox'] });
  const page = await browser.newPage();
  await page.goto('https://www.canva.com', { waitUntil: 'networkidle2' });

  console.log('Nếu chưa đăng nhập, hãy đăng nhập trên cửa sổ browser vừa mở.');
  console.log('Sau khi đăng nhập xong, nhấn Enter ở terminal này để tiếp tục...');
  await new Promise(resolve => process.stdin.once('data', resolve));

  const cookies = await page.cookies();
  const localStorageData = await page.evaluate(() => {
    const out = {};
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i);
      out[k] = localStorage.getItem(k);
    }
    return out;
  });

  fs.writeFileSync('canva_cookies.json', JSON.stringify(cookies, null, 2));
  fs.writeFileSync('canva_localStorage.json', JSON.stringify(localStorageData, null, 2));
  console.log('Đã lưu: canva_cookies.json  và  canva_localStorage.json');
  await browser.close();
})();
