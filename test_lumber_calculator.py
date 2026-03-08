import time
from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    # Need to access through file protocol or start a simple server
    import os
    file_path = f"file://{os.path.abspath('public/lumber-calculator.html')}"
    page.goto(file_path)

    print("Verifying page title and initial state...")
    assert "Lumber Calculator" in page.title()
    assert page.text_content("#res-bf") == "4.40" # 1" * 6" * 8' / 12 * 1 * 1.1 = 4.4
    assert page.text_content("#res-bf-raw") == "4.00"

    print("Testing inputs...")
    page.fill("#lumber-thickness", "2")
    page.fill("#lumber-width", "4")
    page.fill("#lumber-length", "10")
    page.fill("#lumber-qty", "5")
    page.fill("#lumber-waste", "15")
    page.fill("#lumber-cost", "1.50")

    # 2" * 4" * 10' / 12 = 6.666 bf per piece
    # * 5 pieces = 33.333 bf raw
    # * 1.15 waste = 38.333 bf total
    # * $1.50/bf = $57.50 total
    time.sleep(0.5) # Wait for debounce or fast input

    res_bf = page.text_content("#res-bf")
    res_raw = page.text_content("#res-bf-raw")
    res_cost = page.text_content("#res-cost")

    print(f"Results: {res_bf} bf, {res_raw} raw, {res_cost}")
    assert res_bf == "38.33"
    assert res_raw == "33.33"
    assert res_cost == "$57.50"

    print("Testing batch mode...")
    page.click("button.btn-outline") # Add to batch mode
    time.sleep(0.5)

    # Check batch UI appeared
    assert page.is_visible("#batch-section")
    assert page.text_content("#batch-total-bf") == "38.33"
    assert page.text_content("#batch-total-cost") == "$57.50"

    # Add a second item
    page.fill("#lumber-thickness", "1")
    page.fill("#lumber-width", "8")
    page.fill("#lumber-length", "8")
    page.fill("#lumber-qty", "2")
    # 1" * 8" * 8' / 12 * 2 = 10.666 bf
    # * 1.15 waste = 12.266 bf
    page.click("button.btn-outline")
    time.sleep(0.5)

    # Check grand totals
    # 38.333 + 12.266 = 50.60 total
    # 50.60 * 1.50 = 75.90 total cost
    res_total_bf = page.text_content("#batch-total-bf")
    res_total_cost = page.text_content("#batch-total-cost")
    print(f"Grand totals: {res_total_bf} bf, {res_total_cost}")
    assert res_total_bf == "50.60"
    assert res_total_cost == "$75.90"

    print("Testing clear batch...")
    page.click("button.btn-remove") # Clear all
    time.sleep(0.5)

    # Ensure hidden
    assert not page.is_visible("#batch-items > div")

    print("All tests passed!")
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
