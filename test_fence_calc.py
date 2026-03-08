from playwright.sync_api import sync_playwright
import os

html_path = f"file://{os.path.abspath('public/fence-calculator.html')}"

def test_picket_style():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(permissions=['clipboard-read', 'clipboard-write'])
        page = context.new_page()
        page.goto(html_path)

        # Select Picket Fence
        page.select_option('#fence-style', 'picket')
        page.wait_for_timeout(100) # give UI a moment to update

        # Check inputs updated
        height = page.locator('#fence-height').input_value()
        assert height == '4'

        spacing = page.locator('#post-spacing').input_value()
        assert spacing == '8'

        rails = page.locator('#rails-per-section').input_value()
        assert rails == '2'

        picket_width = page.locator('#picket-width').input_value()
        assert picket_width == '3.5'

        picket_gap = page.locator('#picket-gap').input_value()
        assert picket_gap == '2'

        # Test custom calculation trigger
        page.fill('#fence-length', '50')
        page.wait_for_timeout(100)

        posts = page.locator('#res-posts').text_content()
        assert posts == '8' # 50/8 = 6.25 -> 7 sections + 1 = 8 posts

        browser.close()

test_picket_style()
print("Tests passed!")
