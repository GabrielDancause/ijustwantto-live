from playwright.sync_api import sync_playwright
import os

html_path = f"file://{os.path.abspath('public/fence-calculator.html')}"

with sync_playwright() as p:
    browser = p.chromium.launch()
    # Need clipboard permissions if we were testing the copy button in headless
    context = browser.new_context(permissions=['clipboard-read', 'clipboard-write'])
    page = context.new_page()
    page.goto(html_path)

    # Wait for rendering
    page.wait_for_selector('h1:has-text("Fence Calculator")')

    # Take screenshot
    page.screenshot(path="screenshot_fence_calc.png", full_page=True)

    # Check calculated values for the default input (100ft Privacy Fence)
    # Default is Length: 100, Post Spacing: 8 -> 13 Sections -> 14 Posts
    # 3 Rails -> 13*3 = 39 Rails
    # Picket width 5.5, gap 0 -> 96 / 5.5 = ~18 pickets per section. 18 * 13 = 234 pickets
    # 1.5 Concrete bags per post -> 14 * 1.5 = 21 bags

    posts = page.locator('#res-posts').text_content()
    rails = page.locator('#res-rails').text_content()
    pickets = page.locator('#res-pickets').text_content()
    concrete = page.locator('#res-concrete').text_content()
    cost = page.locator('#res-total-cost').text_content()

    print(f"Posts: {posts}")
    print(f"Rails: {rails}")
    print(f"Pickets: {pickets}")
    print(f"Concrete: {concrete}")
    print(f"Total Cost: {cost}")

    browser.close()
