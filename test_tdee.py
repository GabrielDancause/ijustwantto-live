import sys
import os
from playwright.sync_api import sync_playwright

def run_tests():
    print("Running tests for tdee-calculator...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Test index.html contains TDEE Calculator
        page.goto("http://localhost:8000/index.html")
        page.wait_for_selector('text=TDEE Calculator')
        print("Found TDEE Calculator link on index page")

        # Go to the tdee calculator directly
        page.goto("http://localhost:8000/tdee-calculator.html")

        # Wait for form to load
        page.wait_for_selector('form#tdeeForm')

        # Fill the form: 30 years old, 70kg, 175cm, Male, Sedentary, Maintenance, Balanced
        page.fill('#age', '30')
        page.fill('#weight', '70')
        page.fill('#height', '175')
        page.select_option('#activity', '1.2')
        page.select_option('#split', 'balanced')

        # Submit the form
        page.click('button.calculate-btn')

        # Wait for results
        page.wait_for_selector('#bmrValue')

        # Mifflin BMR for male: (10 * 70) + (6.25 * 175) - (5 * 30) + 5 = 700 + 1093.75 - 150 + 5 = 1648.75 ~ 1649
        bmr = page.text_content('#bmrValue')
        print(f"BMR Value: {bmr}")
        assert "1,649" in bmr, f"Expected BMR ~ 1,649, got {bmr}"

        # TDEE for Sedentary (1.2) = 1648.75 * 1.2 = 1978.5 ~ 1979
        tdee = page.text_content('#tdeeValue')
        print(f"TDEE Value: {tdee}")
        assert "1,979" in tdee, f"Expected TDEE ~ 1,979, got {tdee}"

        # Target Calories (Maintenance) = 1979
        target = page.text_content('#targetCalories')
        print(f"Target Calories: {target}")
        assert "1,979" in target, f"Expected Target Calories ~ 1,979, got {target}"

        # Protein (30% of 1978.5 = 593.55 kcal / 4 = 148g)
        protein = page.text_content('#proteinValue')
        print(f"Protein Value: {protein}")
        assert "148" in protein, f"Expected Protein ~ 148, got {protein}"

        # Try changing to Female
        # Wait for the label containing the input to be clicked instead
        page.locator('text=Female').click()
        page.click('button.calculate-btn')
        page.wait_for_selector('#bmrValue')

        # Female BMR: (10 * 70) + (6.25 * 175) - (5 * 30) - 161 = 1482.75 ~ 1483
        bmr_female = page.text_content('#bmrValue')
        print(f"Female BMR Value: {bmr_female}")
        assert "1,483" in bmr_female, f"Expected Female BMR ~ 1,483, got {bmr_female}"

        # Try goal cutting (-500)
        page.locator('text=Cutting (-500 kcal)').click()
        page.click('button.calculate-btn')
        page.wait_for_selector('#targetCalories')

        # TDEE for female: 1482.75 * 1.2 = 1779.3 ~ 1779
        # Cutting target: 1779 - 500 = 1279
        target_cut = page.text_content('#targetCalories')
        print(f"Cutting Target Calories: {target_cut}")
        assert "1,279" in target_cut, f"Expected Target Calories ~ 1,279, got {target_cut}"

        print("All tests passed!")
        browser.close()

if __name__ == "__main__":
    run_tests()
