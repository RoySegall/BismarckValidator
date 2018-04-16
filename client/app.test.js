import puppeteer from 'puppeteer'

const appUrlBase = 'http://localhost:4200/';
const routes = {
  admin: {
    templates: `${appUrlBase}/templates`,
  }
};

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
    await page.goto(routes.private.events)
    await page.waitForSelector('[data-testid="userLoginForm"]')
  })
});
