import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "file://" + os.path.abspath("login.html")

def test_successful_login():
    driver = webdriver.Chrome()
    driver.get(url)

    driver.find_element(By.ID, "username").send_keys("admin")
    driver.find_element(By.ID, "password").send_keys("admin")
    driver.find_element(By.ID, "loginButton").click()

    # todo optimize
    WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element((By.ID, "greeting"), "Welcome, admin!")
    )
    assert "Welcome, admin!" in driver.find_element(By.ID, "greeting").text

    driver.quit()

def test_successful_login_with_press_enter():
    driver = webdriver.Chrome()
    driver.get(url)

    driver.find_element(By.ID, "username").send_keys("admin")
    driver.find_element(By.ID, "password").send_keys("admin" + Keys.ENTER)

    # todo optimize
    WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element((By.ID, "greeting"), "Welcome, admin!")
    )
    assert "Welcome, admin!" in driver.find_element(By.ID, "greeting").text

    driver.quit()

def test_wrong_credentials():
    driver = webdriver.Chrome()
    driver.get(url)

    driver.find_element(By.ID, "username").send_keys("admin")
    driver.find_element(By.ID, "password").send_keys("ad11min" + Keys.ENTER)
    assert "Invalid username or password." in driver.find_element(By.ID, "message").text

    driver.quit()

def test_missing_credentials():
    driver = webdriver.Chrome()
    driver.get(url)

    driver.find_element(By.ID, "loginButton").click()
    assert "Username and Password are required." in driver.find_element(By.ID, "message").text

    driver.quit()

def test_missing_password():
    driver = webdriver.Chrome()
    driver.get(url)

    driver.find_element(By.ID, "username").send_keys("admin" + Keys.ENTER)
    assert "Password is required." in driver.find_element(By.ID, "message").text

    driver.quit()

def test_missing_username():
    driver = webdriver.Chrome()
    driver.get(url)

    driver.find_element(By.ID, "password").send_keys("admin" + Keys.ENTER)
    assert "Username is required." in driver.find_element(By.ID, "message").text

    driver.quit()