import os
from playwright.sync_api import sync_playwright

def verify_drywall_calculator():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Give context permissions for clipboard writing to avoid errors in headless mode
        context = browser.new_context(permissions=['clipboard-read', 'clipboard-write'])
        page = context.new_page()

        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = f"file://{current_dir}/public/drywall-calculator.html"
        page.goto(file_path)

        assert "Drywall Calculator" in page.title(), f"Title mismatch: {page.title()}"

        page.wait_for_selector("#res-sqft")
        initial_sqft = page.inner_text("#res-sqft")
        assert initial_sqft == "490", f"Expected default sqft to be 490, got {initial_sqft}"

        page.fill("#room-length", "15")
        page.wait_for_timeout(50)
        new_sqft = page.inner_text("#res-sqft")
        assert new_sqft == "576", f"Expected new sqft to be 576, got {new_sqft}"

        page.select_option("#calc-mode", "sqft")
        page.wait_for_timeout(50)
        sqft_mode_sqft = page.inner_text("#res-sqft")
        assert sqft_mode_sqft == "550", f"Expected sqft mode to be 550, got {sqft_mode_sqft}"

        page.click("#copy-btn")
        page.wait_for_timeout(500) # Give time for JS to update DOM text
        btn_text = page.inner_text("#copy-btn")
        assert "Copied!" in btn_text, f"Expected button to say Copied!, got {btn_text}"

        print("All Drywall Calculator tests passed successfully!")

        browser.close()

if __name__ == "__main__":
    verify_drywall_calculator()
