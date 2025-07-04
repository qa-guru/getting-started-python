from selene import browser, have

def test_success_login():
    browser.open('https://niffler.qa.guru')
    browser.element('[id="username"]').type('stas')
    browser.element('[id="password"]').type('12345')
    browser.element('[id="login-button"]').click()

    browser.element('[id="spendings"]').should(have.text('History of Spendings'))
    browser.quit()

def test_success_login_with_press_enter():
    browser.open('https://niffler.qa.guru')
    browser.element('[id="username"]').type('stas')
    browser.element('[id="password"]').type('12345').press_enter()

    browser.element('[id="spendings"]').should(have.text('History of Spendings'))
    browser.quit()

def test_wrong_credentials():
    browser.open('https://niffler.qa.guru')
    browser.element('[id="username"]').type('stas')
    browser.element('[id="password"]').type('12345sgsrgwr').press_enter()

    browser.element('[class="form__error"]').should(have.text('Bad credentials'))
    browser.quit()
