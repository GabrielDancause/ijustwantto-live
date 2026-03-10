from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('http://localhost:8000/sleep-calculator.html')
        page.screenshot(path='screenshot-sleep.png', full_page=True)
        browser.close()

if __name__ == '__main__':
    run()
