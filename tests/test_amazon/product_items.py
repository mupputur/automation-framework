import time
from selenium.webdriver.common.by import By



def get_product_details(driver, url):

    driver.get(url)
    time.sleep(2)
    product_title = driver.find_element(By.XPATH, "//*[@id='productTitle']").text
    price = driver.find_element(By.XPATH, "//*[@class='a-section a-spacing-none aok-align-center aok-relative']").text
    brand = driver.find_element(By.XPATH, "(//*[@class='a-size-medium a-text-bold'])[3]").text
    return product_title, price, brand