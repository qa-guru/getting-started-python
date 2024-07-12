from playwright.sync_api import sync_playwright


def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto('https://google.com')
    search_box = page.locator('[name="q"]')
    search_box.fill('yashaka/selene')
    search_box.press('Enter')
    search_results = page.locator('#search')
    search_results.wait_for()
    assert 'Selene - User-oriented Web UI browser tests in Python' in search_results.text_content()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
