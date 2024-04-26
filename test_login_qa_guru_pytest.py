from selene import browser, be, have


def test_valid_login():
    browser.open('https://school.qa.guru')

    browser.element('[name="email"]').type('qagurubot@gmail.com')
    browser.element('[name="password"]').type('somepasshere').press_enter()
    browser.element('[class="page-header"]').should(have.text('Список тренингов'))

    browser.open('https://school.qa.guru/cms/system/login')
    browser.element('.logined-form').should(have.text('QA_GURU_BOT'))
    # browser.close()  TODO Improve tests to run in parallel, move to fixture


def test_wrong_password_login():
    browser.open('https://school.qa.guru')

    browser.element('[name="email"]').type('qagurubot@gmail.com')
    browser.element('[name="password"]').type('123124').press_enter()
    browser.element('.btn-error').should(have.text('Неверный пароль'))
    # browser.close()


def test_empty_password_login():
    browser.open('https://school.qa.guru')

    browser.element('[name="email"]').type('qagurubot@gmail.com')
    browser.element('[name="password"]').type('').press_enter()
    browser.element('.btn-error').should(have.text('Не заполнено поле Пароль'))
    # browser.close()


def test_empty_login():
    browser.open('https://school.qa.guru')

    browser.element('[name="password"]').type('').press_enter()
    browser.element('.btn-error').should(have.text('Не заполнено поле E-Mail'))
    # browser.close()
