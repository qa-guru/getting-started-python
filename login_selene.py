import os

from selene import browser, have

url = "file://" + os.path.abspath("login.html")

def test_successful_login():
    browser.open(url)

    browser.element('[id=username]').type("admin")
    browser.element('[id=password]').type("admin")
    browser.element('[id=loginButton]').click()
    browser.element('[id=greeting]').should(have.text("Welcome, admin!"))

    browser.quit()

def test_successful_login_with_press_enter():
    browser.open(url)
    browser.element('[id=username]').type("admin")
    browser.element('[id=password]').type("admin").press_enter()
    browser.element('[id=greeting]').should(have.text("Welcome, admin!"))

    browser.quit()

def test_wrong_credentials():
    browser.open(url)
    browser.element('[id=username]').type("admin")
    browser.element('[id=password]').type("ad11min").press_enter()
    browser.element('[id=message]').should(have.text("Invalid username or password."))

    browser.quit()

def test_missing_credentials():
    browser.open(url)
    browser.element('[id=loginButton]').click()
    browser.element('[id=message]').should(have.text("Username and Password are required."))

    browser.quit()

def test_missing_password():
    browser.open(url)
    browser.element('[id=username]').type("admin").press_enter()
    browser.element('[id=message]').should(have.text("Password is required."))

    browser.quit()

def test_missing_username():
    browser.open(url)
    browser.element('[id=password]').type("admin").press_enter()
    browser.element('[id=message]').should(have.text("Username is required."))

    browser.quit()