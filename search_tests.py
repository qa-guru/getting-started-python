from selene.support.shared import browser
from selene import by, be, have

browser.open('https://google.com')
browser.element(by.name('q')).should(be.blank).type('selene').press_enter()
browser.element('#search').should(have.text('Selene - User-oriented Web UI browser tests in Python'))