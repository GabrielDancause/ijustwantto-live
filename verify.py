from playwright.sync_api import sync_playwright

def verify_frontend():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto('file:///app/public/list-workout-apps.html')

        # Take a full page screenshot
        page.screenshot(path='/app/screenshot.png', full_page=True)

        # Verify the title
        title = page.title()
        print(f"Title: {title}")

        # Wait a bit for JS
        page.wait_for_timeout(1000)

        browser.close()

if __name__ == "__main__":
    verify_frontend()