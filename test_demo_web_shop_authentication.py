from selene import browser, have, be


def test_successful_login():
    # GIVEN
    browser.open('https://demowebshop.tricentis.com/')

    # WHEN
    browser.element('.ico-login').click()

    # AND
    browser.element('#Email').type('yashaka@gmail.com')
    browser.element('#Password').type('Pa$$w0rd')
    browser.element('.login-button').click()

    # THEN
    browser.element('.header .account').should(have.text('yashaka@gmail.com'))
    browser.element('.ico-logout').should(be.visible)


def test_logout():
    # TODO: implement logout test
    ...
