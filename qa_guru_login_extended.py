import pytest

from selene import browser, have


@pytest.fixture(scope='function', autouse=True)
def browser_management():
    browser.config.base_url = 'https://school.qa.guru'
    # browser.config.timeout = 10
    browser.config.driver_name = 'firefox'

    # driver_options = webdriver.ChromeOptions()
    # driver_options.page_load_strategy = 'eager'


def test_valid_login():
    browser.open('/cms/system/login')
    browser.element('[name=email]').type('qagurubot@gmail.com')
    browser.element('[name=password]').type('somepasshere').press_enter()

    # browser.element('.page-header').should(have.text('Список тренингов'))
    # browser.open('/cms/system/login')

    browser.element('.logined-form').should(have.text('QA_GURU_BOT'))

    browser.quit()


def test_wrong_password():
    browser.open('/cms/system/login')
    browser.element('[name=email]').type('qagurubot@gmail.com')
    browser.element('[name=password]').type('assdaff').press_enter()
    browser.element('.btn-error').should(have.text('Неверный пароль'))

    browser.quit()


def test_empty_password():
    browser.open('/cms/system/login')
    browser.element('[name=email]').type('qagurubot@gmail.com').press_enter()
    browser.element('.btn-error').should(have.text('Не заполнено поле Пароль'))

    browser.quit()


def test_empty_login():
    browser.open('/cms/system/login')
    browser.element('[name=password]').type('assdaff').press_enter()
    browser.element('.btn-error').should(have.text('Не заполнено поле E-Mail'))

    browser.quit()
