const { chromium } = require("playwright");
const fs = require("node:fs/promises");
const path = require("node:path");

(async () => {
  const root = path.resolve(__dirname, "..");
  const reportDir = path.join(root, "_work", "reports");
  await fs.mkdir(reportDir, { recursive: true });

  const url = "https://aws.amazon.com/pt/events/summits/sao-paulo/agenda/";
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ locale: "pt-BR" });
  const responses = [];

  page.on("response", async (response) => {
    const responseUrl = response.url();
    if (!responseUrl.includes("/api/dirs/items/search")) return;
    try {
      const body = await response.text();
      responses.push({ url: responseUrl, status: response.status(), body });
    } catch (error) {
      responses.push({ url: responseUrl, status: response.status(), error: String(error) });
    }
  });

  await page.goto(url, { waitUntil: "networkidle", timeout: 90000 });
  await page.waitForTimeout(5000);

  const text = await page.locator("body").innerText({ timeout: 30000 });
  await fs.writeFile(path.join(reportDir, "aws-agenda-rendered-body.txt"), text, "utf8");
  await fs.writeFile(path.join(reportDir, "aws-agenda-network-responses.json"), JSON.stringify(responses, null, 2), "utf8");

  const sessionMatches = text.match(/[A-Z]{2,5}\d{2,4}/g) || [];
  console.log(JSON.stringify({
    url,
    dirsResponses: responses.map((r) => ({ url: r.url, status: r.status, length: r.body?.length ?? 0 })),
    bodyLength: text.length,
    codeMatches: [...new Set(sessionMatches)].length,
    firstCodes: [...new Set(sessionMatches)].slice(0, 50),
  }, null, 2));

  await browser.close();
})().catch((error) => {
  console.error(error);
  process.exit(1);
});

