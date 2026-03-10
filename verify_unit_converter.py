import time
import sys
import subprocess
from playwright.sync_api import sync_playwright

def verify():
    # Start server in background
    server_process = subprocess.Popen(['python3', '-m', 'http.server', '8000', '-d', '/app/dist'])
    time.sleep(2) # Give server time to start

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(permissions=['clipboard-read', 'clipboard-write'])
            page = context.new_page()

            print("Navigating to unit converter...")
            page.goto('http://localhost:8000/unit-converter.html')
            page.wait_for_load_state('networkidle')

            print("Testing category switch to Weight...")
            page.click('button#btn-weight')
            time.sleep(1)

            print("Setting input to 10...")
            page.fill('input#input-value', '10')
            time.sleep(1)

            print("Taking screenshot...")
            page.screenshot(path='screenshot_unit_converter.png')
            print("Screenshot saved to screenshot_unit_converter.png")

            browser.close()
    finally:
        # Clean up server
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    verify()
