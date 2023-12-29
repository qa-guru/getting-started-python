from selene import browser, be, have, by


def test_selene_can_be_found():
    browser.open('https://google.com')
    if browser.element(by.text('Accept all')).matching(be.visible):
        browser.element(by.text('Accept all')).click()

    browser.element('[name="q"]').should(be.blank).type('yashaka/selene').press_enter()

    browser.element('[id="search"]').should(have.text('Selene - User-oriented Web UI browser tests in Python'))
