from playwright.sync_api import sync_playwright
import os

def test_page():
    with sync_playwright() as p:
        # We need to give permissions for clipboard read/write
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(permissions=['clipboard-read', 'clipboard-write'])
        page = context.new_page()

        # Open local file
        file_path = f"file://{os.path.abspath('public/guide-insulation.html')}"
        page.goto(file_path)

        print("Page loaded")
        # Verify title
        assert "Home Insulation Guide" in page.title()

        # Test Search/Filter: "fiberglass"
        print("Testing search...")
        page.fill('#searchInput', 'fiberglass')
        page.keyboard.press('ArrowUp')

        # Wait a bit
        page.wait_for_timeout(1000)

        # Fiberglass card should be visible
        print("Checking visibility...")

        fiberglass_visible = page.locator('.card', has_text="Fiberglass").is_visible()
        mineral_wool_visible = page.locator('.card', has_text="Mineral Wool").is_visible()

        print(f"Fiberglass visible: {fiberglass_visible}")
        print(f"Mineral Wool visible: {mineral_wool_visible}")
        assert fiberglass_visible
        assert not mineral_wool_visible

        # Clear search input first so table is visible
        page.fill('#searchInput', '')
        page.keyboard.press('ArrowUp')
        page.wait_for_timeout(500)

        # Test copy button (checking if it exists and text changes)
        page.click('#copy-table-btn')
        page.wait_for_timeout(100) # Wait a tiny bit for innerHTML to change
        assert "Copied!" in page.locator('#copy-table-btn').inner_text()

        print("Done!")

        # Take a screenshot
        page.screenshot(path="screenshot_guide_final.png", full_page=True)

        browser.close()

if __name__ == "__main__":
    test_page()