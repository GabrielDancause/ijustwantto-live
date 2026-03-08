from playwright.sync_api import sync_playwright

def test_calculator():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load local HTML file
        import os
        page.goto(f"file://{os.path.abspath('public/btu-calculator.html')}")

        # Fill out form
        page.fill('#length', '20')
        page.fill('#width', '15')
        page.fill('#height', '10') # High ceiling
        page.select_option('#insulation', 'poor') # Poor insulation
        page.select_option('#sun', 'sunny') # Sunny
        page.select_option('#climate', 'cold') # Cold climate
        page.select_option('#kitchen', 'no')

        # Calculate
        page.click('button.calculate-btn')

        # Get results
        cooling = page.inner_text('#coolingBtuValue')
        heating = page.inner_text('#heatingBtuValue')
        area = page.inner_text('#areaValue')
        volume = page.inner_text('#volumeValue')

        print(f"Cooling BTU: {cooling}")
        print(f"Heating BTU: {heating}")
        print(f"Area: {area}")
        print(f"Volume: {volume}")

        assert area == "300", "Area mismatch"
        assert volume == "3,000", "Volume mismatch"

        browser.close()

if __name__ == "__main__":
    test_calculator()