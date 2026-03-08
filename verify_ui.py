from playwright.sync_api import sync_playwright
import os

def test_calculator():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Open local file
        filepath = os.path.abspath('public/solar-calculator.html')
        page.goto(f'file://{filepath}')

        # Verify title
        assert "Solar Panel Calculator" in page.title()

        # Fill in form
        page.fill('#monthlyEnergy', '1000')
        page.fill('#sunlightHours', '5')
        page.fill('#panelWattage', '400')
        page.fill('#electricityRate', '0.15')
        page.fill('#systemCost', '3.0')

        # Submit
        page.click('button[type="submit"]')

        # Wait for results to be visible
        page.wait_for_selector('#results.active')

        # Verify results
        system_size = page.inner_text('#systemSize')
        panels_needed = page.inner_text('#panelsNeeded')

        print(f"System Size: {system_size} kW")
        print(f"Panels Needed: {panels_needed}")

        assert system_size != "0"
        assert panels_needed != "0"

        page.screenshot(path='solar-calc-result.png', full_page=True)
        print("Screenshot saved to solar-calc-result.png")

        browser.close()

if __name__ == "__main__":
    test_calculator()
