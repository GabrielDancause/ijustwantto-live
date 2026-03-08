import time
from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 800})

        # Navigate to the local file
        page.goto("file:///app/public/list-standing-desks.html")

        # Wait a bit for fonts to load
        time.sleep(2)

        # Take a screenshot
        page.screenshot(path="screenshot_standing_desks.png", full_page=True)

        browser.close()

if __name__ == "__main__":
    main()
