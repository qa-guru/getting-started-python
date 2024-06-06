from selene import browser, have


browser.open('https://google.com')
browser.element('[name=q]').type('yashaka/selene').press_enter()
browser.element('#search').should(have.text('Selene - User-oriented Web UI browser tests in Python'))
