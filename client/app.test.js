const puppeteer = require('puppeteer');
const appUrlBase = 'http://localhost:4200/';
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

describe('private routes', () => {
  test('redirects to login route when logged out', async () => {
    await page.goto(appUrlBase);
    await page.waitForSelector('[data-testid="userLoginForm"]')
  })
});

afterAll(() => {
  if (!process.env.DEBUG) {
    browser.close();
  }
});
