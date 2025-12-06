import { test, expect } from "@playwright/test";

const BASE_URL = "http://127.0.0.1:8000/static/index.html";

test.describe("Calculations BREAD UI", () => {
  test("creates a calculation and shows it in the table", async ({ page }) => {
    await page.goto(BASE_URL);

    const rows = page.locator("#calc-tbody tr");
    const initialCount = await rows.count();

    // Fill form
    await page.selectOption("#operation", "add");
    await page.fill("#a", "10");
    await page.fill("#b", "5");

    // Click submit and wait for POST /calculations
    await Promise.all([
      page.click("#submit-btn"),
      page.waitForResponse((response) =>
        response.url().endsWith("/calculations") &&
        response.request().method() === "POST"
      ),
    ]);

    // We should have one more row
    await expect(rows).toHaveCount(initialCount + 1);

    // Newest row (appends at end)
    const newRow = rows.nth(initialCount);

    // Should include operation and operands
    await expect(newRow).toContainText("add");
    await expect(newRow).toContainText("10");
    await expect(newRow).toContainText("5");
  });

  test("shows validation error when fields are empty", async ({ page }) => {
    await page.goto(BASE_URL);

    // Ensure fields are empty
    await page.fill("#a", "");
    await page.fill("#b", "");

    // Submit
    await page.click("#submit-btn");

    // Our JS validation should show an error message
    const error = page.locator("#error-msg");
    await expect(error).toContainText("required", { ignoreCase: true });
  });
});
