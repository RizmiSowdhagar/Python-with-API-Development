import { test, expect } from "@playwright/test";

test("shows login required message on usage summary page", async ({ page }) => {
  // Open the usage summary page
  await page.goto("http://127.0.0.1:8000/static/report.html");

  // Click the button that calls /reports/summary
  await page.click("#show-stats-btn");

  // Wait a moment for the DOM to update
  await page.waitForTimeout(1000);

  // The page should tell the user they must be logged in
  const totalText = await page.textContent("#stats-total");
  expect(totalText).toContain("You must be logged in to see the report.");
});
