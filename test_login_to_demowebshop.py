from selene import browser, have

browser.config.timeout = 2


def open_login_form():
    browser.open('https://demowebshop.tricentis.com/')
    browser.element('.ico-login').click()


def test_valid_login():
    open_login_form()

    browser.element('#Email').type('yashaka@gmail.com')
    browser.element('#Password').type('Pa$$w0rd')
    browser.element('.login-button').click()

    browser.element('.header .account').should(have.exact_text('yashaka'))


def test_logout():
    ...
