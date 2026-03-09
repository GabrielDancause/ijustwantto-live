import os
from playwright.sync_api import sync_playwright

def verify_protein_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Get absolute path for local file
        file_path = f"file://{os.path.abspath('public/protein-per-dollar.html')}"

        print(f"Navigating to {file_path}")
        page.goto(file_path)

        # Wait for JS to render cards
        page.wait_for_selector('.card')

        # Take initial screenshot
        page.screenshot(path="screenshot_protein_initial.png", full_page=True)
        print("Took initial screenshot: screenshot_protein_initial.png")

        # Interact with the category filter
        page.select_option('#category-filter', 'legume')
        page.wait_for_timeout(500)  # Wait for animation/render

        # Take filtered screenshot
        page.screenshot(path="screenshot_protein_filtered.png")
        print("Took filtered screenshot: screenshot_protein_filtered.png")

        browser.close()

if __name__ == "__main__":
    verify_protein_page()
