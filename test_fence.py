import time
from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        file_path = f"file://{os.path.abspath('public/fence-calculator.html')}"
        print(f"Loading {file_path}")
        page.goto(file_path)

        # Allow time for initial calculation
        page.wait_for_timeout(1000)

        # Check default calculations
        print("Checking default calculation...")
        posts = page.locator("#res-posts").text_content()
        rails = page.locator("#res-rails").text_content()
        pickets = page.locator("#res-pickets").text_content()
        concrete = page.locator("#res-concrete").text_content()
        total_cost = page.locator("#res-total-cost").text_content()

        print(f"Posts: {posts}")
        print(f"Rails: {rails}")
        print(f"Pickets: {pickets}")
        print(f"Concrete: {concrete}")
        print(f"Total Cost: {total_cost}")

        # Change input values to verify reactivity
        print("\nChanging input values (200ft fence)...")
        page.fill("#fence-length", "200")

        # Allow time for calculation
        page.wait_for_timeout(500)

        # Check updated calculations
        posts_updated = page.locator("#res-posts").text_content()
        rails_updated = page.locator("#res-rails").text_content()
        pickets_updated = page.locator("#res-pickets").text_content()
        concrete_updated = page.locator("#res-concrete").text_content()
        total_cost_updated = page.locator("#res-total-cost").text_content()

        print(f"Updated Posts: {posts_updated}")
        print(f"Updated Rails: {rails_updated}")
        print(f"Updated Pickets: {pickets_updated}")
        print(f"Updated Concrete: {concrete_updated}")
        print(f"Updated Total Cost: {total_cost_updated}")

        # Take a screenshot
        screenshot_path = "screenshot.png"
        page.screenshot(path=screenshot_path, full_page=True)
        print(f"\nScreenshot saved to {screenshot_path}")

        browser.close()

if __name__ == "__main__":
    run()