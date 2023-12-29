from selene import browser, be, have


def test_fail_to_login_with_wrong_password():
    browser.open('https://qa.guru/cms/system/login')

    browser.element('.login-form [name=email]').type('qagurubot@gmail.com')
    browser.element('.login-form [name=password]').type('wrong-password')
    browser.element('.login-form .btn-success').click()

    browser.element('.login-form .btn-success.btn-error').should(be.visible)
    browser.element('.login-form .btn-success.btn-error').with_(timeout=6).should(be.hidden)


def test_successful_login_with_correct_password():
    ...
    # TODO: implement
