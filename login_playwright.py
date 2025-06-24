import os
from playwright.sync_api import sync_playwright

url = "file://" + os.path.abspath("login.html")

def test_successful_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)

        page.fill('#username', 'admin')
        page.fill('#password', 'admin')
        page.click('#loginButton')
        page.wait_for_selector('#greeting')
        assert page.inner_text('#greeting') == 'Welcome, admin!'

        browser.close()

def test_successful_login_with_press_enter():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)

        page.fill('#username', 'admin')
        page.fill('#password', 'admin')
        page.press('#password', 'Enter')
        page.wait_for_selector('#greeting')
        assert page.inner_text('#greeting') == 'Welcome, admin!'

        browser.close()

def test_wrong_credentials():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)

        page.fill('#username', 'admin')
        page.fill('#password', 'ad11min')
        page.press('#password', 'Enter')
        page.wait_for_selector('#message')
        assert page.inner_text('#message') == 'Invalid username or password.'

        browser.close()

def test_missing_credentials():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)

        page.click('#loginButton')
        page.wait_for_selector('#message')
        assert page.inner_text('#message') == 'Username and Password are required.'

        browser.close()

def test_missing_password():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)

        page.fill('#username', 'admin')
        page.press('#username', 'Enter')
        page.wait_for_selector('#message')
        assert page.inner_text('#message') == 'Password is required.'

        browser.close()

def test_missing_username():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)

        page.fill('#password', 'admin')
        page.press('#password', 'Enter')
        page.wait_for_selector('#message')
        assert page.inner_text('#message') == 'Username is required.'

        browser.close()