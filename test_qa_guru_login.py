import pytest
from selene import browser, have, be
from selenium import webdriver


@pytest.fixture(scope='function', autouse=True)
def browser_management():
    driver_options = webdriver.ChromeOptions()
    driver_options.page_load_strategy = 'eager'
    browser.config.driver_options = driver_options


def test_valid_login():
    browser.open('https://school.qa.guru')
    browser.element('[name="email"]').should(be.blank).type('qagurubot@gmail.com')
    browser.element('[name="password"]').type('somepasshere').press_enter()
    browser.open('https://school.qa.guru/cms/system/login')
    browser.element('.logined-form').should(have.text('Здравствуйте, QA_GURU_BOT'))


def test_invalid_login_with_wrong_password():
    browser.open('https://school.qa.guru')
    browser.element('[name="email"]').should(be.blank).type('qagurubot@gmail.com')
    browser.element('[name="password"]').type('sdfds').press_enter()
    browser.element('.btn-success').should(have.text('Неверный пароль'))
