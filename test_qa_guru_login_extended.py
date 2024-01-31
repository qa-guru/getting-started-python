from selene import browser, have, be


def test_valid_login():
    browser.open('https://school.qa.guru')
    browser.element('[name="email"]').should(be.blank).type('qagurubot@gmail.com')
    browser.element('[name="password"]').type('somepasshere').press_enter()
    browser.open('https://school.qa.guru/cms/system/login')
    browser.element('.logined-form').should(have.text('Здравствуйте, QA_GURU_BOT'))