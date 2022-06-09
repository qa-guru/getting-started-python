from selene.support.shared import browser
from selene import be, have


browser.open('https://google.com')
browser.element('[name="q"]').should(be.blank).type('selene').press_enter()
browser.element('[id="search"]').should(have.text('Selene - User-oriented Web UI browser tests in Python'))
