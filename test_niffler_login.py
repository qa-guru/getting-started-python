from selene import browser, be, have


def test_success_login():
    browser.open("https://niffler.qa.guru")
    browser.element('[id="username"]').should(be.blank).type('stas')
    browser.element('[id="password"]').type('12345').press_enter()
    browser.element('[id="spendings"]').should(have.text('History of Spendings'))
