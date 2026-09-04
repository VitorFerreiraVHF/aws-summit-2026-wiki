const { chromium } = require("playwright");
const fs = require("node:fs/promises");
const path = require("node:path");

(async () => {
  const root = path.resolve(__dirname, "..");
  const reportDir = path.join(root, "_work", "reports");
  await fs.mkdir(reportDir, { recursive: true });

  const directoryId = "events-cards-interactive-summits-summit-saopaulo-2026-summit-saopaulo-2026-2026-08-31-2";
  const pageUrl = "https://aws.amazon.com/pt/events/summits/sao-paulo/agenda/";
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ locale: "pt-BR" });
  await page.goto(pageUrl, { waitUntil: "networkidle", timeout: 90000 });

  const result = await page.evaluate(async ({ directoryId }) => {
    const sizesToProbe = [1, 5, 10, 20, 50, 100, 200, 500];
    const probes = [];
    async function request(size, pageNumber = undefined) {
      const params = new URLSearchParams({
        "item.directoryId": directoryId,
        "item.locale": "en_US",
        "sort_by": "item.additionalFields.publishedDate",
        "sort_order": "asc",
        "size": String(size),
      });
      if (pageNumber !== undefined) params.set("page", String(pageNumber));
      const response = await fetch(`/api/dirs/items/search?${params.toString()}`, {
        method: "GET",
        mode: "cors",
        credentials: "include",
        headers: { Accept: "application/json" },
      });
      const buffer = await response.arrayBuffer();
      const body = new TextDecoder("windows-1252").decode(buffer);
      let json;
      try {
        json = JSON.parse(body);
      } catch {
        json = null;
      }
      return { status: response.status, url: response.url, body, count: json?.metadata?.count, totalHits: json?.metadata?.totalHits, items: json?.items?.length };
    }
    for (const size of sizesToProbe) {
      probes.push(await request(size));
    }
    const workingSize = probes.find((probe) => (probe.items || 0) > 0)?.items || 1;
    const first = probes.find((probe) => (probe.items || 0) > 0) || probes[0];
    const total = first.totalHits || first.count || first.items || 0;
    const size = Math.max(1, Math.min(workingSize, 50));
    const pages = [];
    const pageCount = Math.max(1, Math.ceil(total / size));
    for (let pageNumber = 0; pageNumber < pageCount; pageNumber++) {
      pages.push(await request(size, pageNumber));
    }
    return { probes, pages };
  }, { directoryId });

  await fs.writeFile(path.join(reportDir, "aws_dirs_items_search_full_browser_probe.json"), JSON.stringify(result, null, 2), "utf8");
  const parsedItems = [];
  for (const pageResult of result.pages || []) {
    try {
      const parsed = JSON.parse(pageResult.body);
      for (const item of parsed.items || []) parsedItems.push(item);
    } catch {}
  }
  await fs.writeFile(
    path.join(reportDir, "aws_dirs_items_search_full_browser.json"),
    JSON.stringify({ items: parsedItems, metadata: { count: parsedItems.length, totalHits: parsedItems.length } }, null, 2),
    "utf8",
  );
  console.log(JSON.stringify({
    probes: result.probes.map(({ status, url, count, totalHits, items, body }) => ({ status, url, count, totalHits, items, bodyLength: body.length })),
    pages: result.pages.map(({ status, count, totalHits, items, body }, index) => ({ page: index, status, count, totalHits, items, bodyLength: body.length })),
    collectedItems: parsedItems.length,
  }, null, 2));

  await browser.close();
})().catch((error) => {
  console.error(error);
  process.exit(1);
});
