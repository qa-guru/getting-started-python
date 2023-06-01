from selene import browser, have

browser.config.timeout = 6


def test_login_to_cms_with_valid_credentials():
    browser.open('https://qa.guru/cms/system/login')
    browser.element('.login-form [name=email]').type('qagurubot@gmail.com')
    browser.element('.login-form [name=password]').type('qagurupassword').press_enter()

    browser.element('.main-header__login').click()
    browser.element('.logined-form').should(have.text('QA_GURU_BOT'))
    browser.should(have.url_containing('/cms/system/login'))
