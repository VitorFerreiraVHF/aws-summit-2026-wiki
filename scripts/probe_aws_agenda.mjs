import { chromium } from "playwright";
import fs from "node:fs/promises";
import path from "node:path";

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const reportDir = path.join(root.replace(/^\/([A-Za-z]:)/, "$1"), "_work", "reports");
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

const cards = await page.locator("text=/\\| [A-Z]{2,5}\\d{2,4}/").count().catch(() => 0);
const sessionMatches = text.match(/[A-Z]{2,5}\\d{2,4}/g) || [];
console.log(JSON.stringify({
  url,
  dirsResponses: responses.map((r) => ({ url: r.url, status: r.status, length: r.body?.length ?? 0 })),
  bodyLength: text.length,
  codeMatches: [...new Set(sessionMatches)].length,
  cardLikeMatches: cards,
  firstCodes: [...new Set(sessionMatches)].slice(0, 30),
}, null, 2));

await browser.close();

