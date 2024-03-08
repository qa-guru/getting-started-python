import pytest
from selene import browser, have, be


@pytest.fixture(scope='function', autouse=True)
def browser_management():
    browser.config.driver_name = 'firefox'
    browser.config.base_url = 'https://school.qa.guru'


def test_valid_login():
    browser.open('/')
    browser.element('[name="email"]').should(be.blank).type('qagurubot@gmail.com')
    browser.element('[name="password"]').should(be.blank).type('somepasshere').press_enter()
    browser.element('.page-header').should(have.text('Список тренингов'))

    browser.open('/cms/system/login')
    browser.element('.logined-form').should(have.text('QA_GURU_BOT'))

