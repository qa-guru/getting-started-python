from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.implicitly_wait(10)

driver.get('https://github.com/search')
driver.find_element(By.CSS_SELECTOR, '[aria-label="Search GitHub"]').send_keys('qa.guru', Keys.RETURN)

search_results = driver.find_element(By.CSS_SELECTOR, '[data-testid="results-list"]')
assert 'QA.GURU' in search_results.text

driver.quit()
