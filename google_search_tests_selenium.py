from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


def test_captcha_should_be_shown():
    driver = webdriver.Chrome()
    driver.get('https://google.com')

    search_input = driver.find_element(By.NAME, 'q')
    search_input.send_keys('qa.guru')
    search_input.send_keys(Keys.RETURN)

    time.sleep(2)  # Подождать загрузку страницы (лучше заменить на WebDriverWait)

    assert 'About this page' in driver.page_source
    driver.quit()