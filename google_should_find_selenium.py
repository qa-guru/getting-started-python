from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.implicitly_wait(10)

driver.get('https://google.com')
driver.find_element(By.NAME, 'q').send_keys('yashaka/selene', Keys.RETURN)

search_results = driver.find_element(By.ID, 'search')
assert 'Selene - User-oriented Web UI browser tests in Python' in search_results.text

driver.quit()
