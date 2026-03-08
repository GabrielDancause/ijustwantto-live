from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch()
    page = browser.new_page()
    page.goto("file:///app/dist/deck-calculator.html")

    # Check that title matches
    assert "Deck Board Calculator" in page.title()

    # Fill in the form
    page.fill("#deck-width", "20")
    page.fill("#deck-depth", "16")
    page.select_option("#board-width", "5.5")
    page.select_option("#board-length", "16")
    page.select_option("#joist-spacing", "16")

    # Since there's an oninput/onchange trigger, wait for a tick or fire event manually if needed.
    # Playwright's fill/select_option usually fires change events.
    page.wait_for_timeout(500)

    # Assert values
    area = page.locator("#res-area").inner_text()
    boards = page.locator("#res-boards").inner_text()

    print(f"Calculated Area: {area}")
    print(f"Calculated Boards: {boards}")

    # Area = 20 * 16 = 320
    assert area == "320"

    page.screenshot(path="screenshot.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
