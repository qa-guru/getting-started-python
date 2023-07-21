from selene import browser, have

browser.config.timeout = 8


def teardown_function():
    browser.quit()


def test_valid_login():
    browser.open('https://qa.guru/cms/system/login')

    browser.element('.login-form [name=email]').type('qagurubot@gmail.com').press_tab()
    browser.element('[name=password]').type('qagurupassword').press_enter()

    browser.element('.main-header__login').click()
    browser.element('.logined-form').should(have.text('QA_GURU_BOT'))


def test_invalid_login_with_wrong_password():
    browser.open('https://qa.guru/cms/system/login')

    browser.element('.login-form [name=email]').type('qagurubot@gmail.com').press_tab()
    browser.element('[name=password]').type('abracadabra').press_enter()

    browser.element('.login-form .btn-success').should(have.exact_text('Неверный пароль'))


def test_invalid_login_with_empty_password():
    browser.open('https://qa.guru/cms/system/login')

    browser.element('.login-form [name=email]').type('qagurubot@gmail.com').press_enter()

    browser.element('.login-form .btn-success').should(have.exact_text('Не заполнено поле Пароль'))

