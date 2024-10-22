# selenium 4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import time 

service = Service('/usr/local/bin/chromedriver')  # Replace with the actual path
driver = webdriver.Chrome(service=service)
driver.get("https://www.bistek.com.br/mercearia")
driver.execute_script("window.scrollTo(0, 1000)")
time.sleep(10)
grocery_name = driver.find_elements(By.CLASS_NAME, 'vtex-product-summary-2-x-brandName')
for name in grocery_name:
    print(name.text)
driver.quit()