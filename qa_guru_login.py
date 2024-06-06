from selene import browser, have


def test_valid_login():
    browser.open('https://school.qa.guru/cms/system/login')
    browser.element('[name=email]').type('qagurubot@gmail.com')
    browser.element('[name=password]').type('somepasshere').press_enter()
    browser.element('.logined-form').should(have.text('QA_GURU_BOT'))

    browser.quit()


def test_wrong_password():
    browser.open('https://school.qa.guru/cms/system/login')
    browser.element('[name=email]').type('qagurubot@gmail.com')
    browser.element('[name=password]').type('assdaff').press_enter()
    browser.element('.btn-error').should(have.text('Неверный пароль'))

    browser.quit()


def test_empty_password():
    browser.open('https://school.qa.guru/cms/system/login')
    browser.element('[name=email]').type('qagurubot@gmail.com').press_enter()
    browser.element('.btn-error').should(have.text('Не заполнено поле Пароль'))

    browser.quit()


def test_empty_login():
    browser.open('https://school.qa.guru/cms/system/login')
    browser.element('[name=password]').type('assdaff').press_enter()
    browser.element('.btn-error').should(have.text('Не заполнено поле E-Mail'))

    browser.quit()
