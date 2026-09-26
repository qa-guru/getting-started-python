from playwright.sync_api import sync_playwright, expect


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto('https://github.com/search')
    search_box = page.locator('[aria-label="Search GitHub"]')
    search_box.fill('qa.guru')
    search_box.press('Enter')

    expect(page.locator('[data-testid="results-list"]')).to_contain_text('QA.GURU')

    browser.close()
