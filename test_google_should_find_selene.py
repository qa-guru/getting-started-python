from time import sleep

from selene.support.shared import browser
from selene import be, have
import pytest

@pytest.fixture()
def brows():
    browser.open('https://google.com')

def test1(brows):
    browser.element('[name="q"]').should(be.blank).type('yashaka/selene').press_enter()
    browser.element('[id="search"]').should(have.text('Selene - User-oriented Web UI browser tests in Python'))
    print ("По запросу найдена ссылка")


def test2(brows):
    browser.element('[name="q"]').should(be.blank).type('yashaka/selene').press_enter()
    assert browser.element('[id="search"]') != 'qmkugnj ,.'
    print ("По запросу ничего не найдено")