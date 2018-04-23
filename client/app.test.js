const puppeteer = require('puppeteer');
const appUrlBase = 'http://127.0.0.1:4200';
let browser;
let page;
beforeAll(async () => {
  browser = await puppeteer.launch(
    process.env.DEBUG
      ? {
          headless: false,
          slowMo: 100,
        }
      : {}
  );

  page = await browser.newPage()
});

describe('Uploads', () => {
  test('Testing the upload process.', async () => {
    await page.goto(appUrlBase);
    await page.waitForSelector('form#upload');
    let dropZoneInput = await page.$('.dz-hidden-input');
    dropZoneInput.uploadFile(process.cwd() + '/../pytest_assets/513026484_gs.xlsx');
    await page.waitForSelector('#checkFiles');
    await page.click('#checkFiles');
    await page.waitForSelector('.folder-view');
  });

  test('Testing the folder view', async () => {
    await page.waitForSelector('.folder-view');
  });
});

afterAll(() => {
  if (!process.env.DEBUG) {
    browser.close();
  }
});
