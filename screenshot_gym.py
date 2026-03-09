import os
from playwright.sync_api import sync_playwright

def verify_gym_costs():
    filepath = os.path.abspath('public/gym-costs.html')
    url = f"file://{filepath}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the page
        page.goto(url)

        # Wait for the table to populate (it happens immediately via inline script but just to be sure)
        page.wait_for_selector('table')

        # Verify Key Stats exist
        assert page.locator('#stat-count').is_visible()

        # Verify JSON-LD Schema
        schema = page.locator('script[type="application/ld+json"]').inner_text()
        assert "Article" in schema
        assert "FAQPage" in schema

        # Scroll a bit and take a full page screenshot
        page.screenshot(path="screenshot_gym_costs.png", full_page=True)

        print("Frontend verification complete. Screenshot saved as screenshot_gym_costs.png")
        browser.close()

if __name__ == "__main__":
    verify_gym_costs()