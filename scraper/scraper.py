from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import time 

service = Service('/usr/local/bin/chromedriver')  
driver = webdriver.Chrome(service=service)
driver.get("https://www.bistek.com.br/mercearia")
driver.execute_script("window.scrollTo(0, 1000)")

time.sleep(10)

grocery_name = driver.find_elements(By.CLASS_NAME, 'vtex-product-summary-2-x-brandName')
grocery_price_reais = driver.find_elements(By.CLASS_NAME, 'vtex-product-price-1-x-currencyInteger')
grocery_price_cents = driver.find_elements(By.CLASS_NAME, 'vtex-product-price-1-x-currencyFraction')

groceries = {}
loop_count = 0
for grocery in grocery_name:
    grocery_name_loop = grocery_name[loop_count].text
    grocery_price_reais_loop = grocery_price_reais[loop_count].text
    grocery_price_cents_loop = grocery_price_cents[loop_count].text
    groceries.update({grocery_name_loop:{'name': grocery_name_loop, 'price_reais': grocery_price_reais_loop, 'price_cents': grocery_price_cents_loop}})
    loop_count += 1

count = 0
for item in groceries:
    count +=1
groceries.update({"count": count})

driver.quit()   