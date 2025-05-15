from playwright.sync_api import sync_playwright


def test_captcha_should_be_shown():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://google.com")

        # Ввод запроса и выполнение поиска
        search_input = page.locator("input[name='q']")
        search_input.fill("qa.guru")
        search_input.press("Enter")

        # Проверка на наличие текста, указывающего на капчу
        assert "About this page" in page.content()

        browser.close()