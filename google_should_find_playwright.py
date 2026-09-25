from playwright.sync_api import sync_playwright, expect


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto('https://google.com')
    search_box = page.locator('[name="q"]')
    search_box.fill('yashaka/selene')
    search_box.press('Enter')

    search_results = page.locator('#search')
    expect(search_results).to_contain_text(
        'Selene - User-oriented Web UI browser tests in Python'
    )

    browser.close()
