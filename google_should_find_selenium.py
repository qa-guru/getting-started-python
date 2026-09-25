from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


with webdriver.Chrome() as driver:
    driver.get('https://google.com')

    search_box = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, 'q'))
    )
    search_box.send_keys('yashaka/selene')
    search_box.send_keys(Keys.RETURN)

    search_results = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'search'))
    )

    assert 'Selene - User-oriented Web UI browser tests in Python' in search_results.text
