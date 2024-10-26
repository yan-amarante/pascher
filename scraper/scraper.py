from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 
import sys

service = Service('/usr/local/bin/chromedriver')  
driver = webdriver.Chrome(service=service)
driver.get("https://www.bistek.com.br/mercearia")

current_element = driver.find_element(By.XPATH, "//li[contains(@class, 'bistek-custom-apps-0-x-paginationItem--ellipsis')]")
last_page = current_element.find_element(By.XPATH, "following-sibling::*[1]")
products_per_page_element = driver.find_element(By.CLASS_NAME, "vtex-search-result-3-x-showingProductsCount")
number_of_pages = last_page.text
products_per_page =  products_per_page_element.text[:2]
time.sleep(10)

def scroll_to_bottom():
    SCROLL_PAUSE_TIME = 10

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    #while True:
        # Scroll down to bottom
    time.sleep(SCROLL_PAUSE_TIME)
    driver.execute_script("window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })")

        # Wait to load page

        # Calculate new scroll height and compare with last scroll height
        # = driver.execute_script("return document.body.scrollHeight")
        #if new_height == last_height:
        #    break
        #last_height = new_height

def scrape_page():
    #driver.execute_script("window.scrollTo(0, 1000)")
    scroll_to_bottom()
    #time.sleep(10)
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
    return groceries

groceries = scrape_page()
page_count = 1
print({"number_of_pages": number_of_pages, "products_per_page":products_per_page,"products_scraped": len(groceries), "pages_scraped": page_count}, flush=True)
while True:
    try:
        # Find the next button (or pagination items)
        wait = WebDriverWait(driver, 10)

        next_button_list = driver.find_elements(By.CLASS_NAME, "bistek-custom-apps-0-x-paginationItemLink")

        # Check if there is a next page
        found_next_page = False
        for page in next_button_list:
            next_page = page_count + 1
            if page.text.isdigit() and int(page.text) == next_page:
                page_count += 1

                query = f"//a[contains(@class, 'bistek-custom-apps-0-x-paginationItemLink') and text()='{next_page}']"

                # Scrape the next page
                next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, query)))
                driver.execute_script("arguments[0].scrollIntoView();", next_button)
                driver.execute_script("arguments[0].click();", next_button)
                
                groceries.update(scrape_page())
                print({"number_of_pages": number_of_pages, "products_per_page":products_per_page,"products_scraped": len(groceries), "pages_scraped": page_count}, flush=True)
                # Scroll to the button and click it
                found_next_page = True
                break

        # If no next page is found, break the loop
        if not found_next_page:
            break

    except Exception as e:
        print(f"An error occurred: {e}")
        break


count = len(groceries)
groceries.update({"count": count})
print(len(groceries))
print(page_count)
driver.quit()   