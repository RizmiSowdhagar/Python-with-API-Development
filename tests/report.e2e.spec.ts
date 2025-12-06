import { test, expect } from "@playwright/test";

test("user can see usage summary", async ({ page }) => {
  await page.goto("http://127.0.0.1:8000/static/report.html");

  // Click the button that calls /reports/summary
  await page.click("#show-stats-btn");

  // Wait a moment for the network call and DOM update
  await page.waitForTimeout(1000);

  const totalText = await page.textContent("#stats-total");
  expect(totalText).toContain("Total calculations:");
});
