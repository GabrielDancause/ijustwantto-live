import os
from playwright.sync_api import sync_playwright

def verify_ui():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the newly created file using absolute path as required by memory
        file_path = "file:///app/public/list-air-purifiers.html"
        page.goto(file_path)

        # 1. Verify CSS Rules
        # Check background color of the body
        bg_color = page.evaluate("window.getComputedStyle(document.body).backgroundColor")
        # rgb(6, 12, 10) is the rgb equivalent of #060c0a
        assert bg_color == "rgb(6, 12, 10)", f"Expected bg color rgb(6, 12, 10), got {bg_color}"

        # Check font family of body
        font_family = page.evaluate("window.getComputedStyle(document.body).fontFamily")
        assert "Inter" in font_family, f"Expected font family to include 'Inter', got {font_family}"

        # 2. Verify Filter Functionality
        # Ensure initially 6 cards are visible
        visible_cards = page.locator(".card:not(.hidden)").count()
        assert visible_cards == 6, f"Expected 6 visible cards initially, found {visible_cards}"

        # Type 'Coway' into the search input
        search_input = page.locator("#searchInput")
        search_input.fill("Coway")

        # After filtering, exactly 1 card should be visible
        visible_cards_after_search = page.locator(".card:not(.hidden)").count()
        assert visible_cards_after_search == 1, f"Expected 1 visible card after search, found {visible_cards_after_search}"

        # Type gibberish to show no results message
        search_input.fill("asdfasdfasdf")

        # Verify no results message is displayed
        no_results_display = page.evaluate("window.getComputedStyle(document.getElementById('noResults')).display")
        assert no_results_display == "block", f"Expected 'noResults' message to be visible (display: block), got {no_results_display}"

        # Verify 0 cards visible
        visible_cards_empty_search = page.locator(".card:not(.hidden)").count()
        assert visible_cards_empty_search == 0, f"Expected 0 visible cards after empty search, found {visible_cards_empty_search}"

        # 3. Emulate mobile and check responsiveness
        # iPhone 12/13 Pro dimensions
        page.set_viewport_size({"width": 390, "height": 844})

        # Ensure grid changed to 1 column by checking grid-template-columns
        # We need to evaluate the computed style of the .card-grid element
        grid_columns = page.evaluate("window.getComputedStyle(document.querySelector('.card-grid')).gridTemplateColumns")
        # We might not get exactly '1fr' or 'minmax(...)', but we can check the number of columns by splitting the string.
        # But wait, we hid all cards. Let's clear search first.
        search_input.fill("")
        grid_columns = page.evaluate("window.getComputedStyle(document.querySelector('.card-grid')).gridTemplateColumns")
        # If it's a single column, it usually computes to something like '358px' (width of the container minus padding)
        # Checking if it's a single value (no spaces)
        assert len(grid_columns.split(" ")) == 1, f"Expected 1 column grid, got {grid_columns}"

        print("UI Verification Passed!")
        browser.close()

if __name__ == "__main__":
    verify_ui()
