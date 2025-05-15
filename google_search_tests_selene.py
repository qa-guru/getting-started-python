from selene import browser, have


def test_captcha_should_be_shown():
    browser.open('https://google.com')
    browser.element('[name="q"]').type('qa.guru').press_enter()
    browser.element('html').should(have.text('About this page'))
