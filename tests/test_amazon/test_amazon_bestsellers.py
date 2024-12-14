import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import tabulate


# Path to ChromeDriver
@pytest.fixture(scope="module")
def driver():
    s = Service(executable_path="C:\\Users\\DELL\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe")
    driver = webdriver.Chrome(service=s)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture(scope="module")
def product_links(driver):
    # Open Amazon website and navigate to Best Sellers in Clothing & Accessories
    driver.get("https://www.amazon.in")
    time.sleep(3)
    best_sellers_section = driver.find_element(By.XPATH, "//*[text()='Best Sellers in Clothing & Accessories']")
    best_sellers_section.click()
    time.sleep(3)

    # Extract product links dynamically
    product_elements = driver.find_elements(By.XPATH, "//*[@class='a-unordered-list a-nostyle a-horizontal feed-carousel-shelf']/li")
    links = []
    for element in product_elements:
        link = element.find_element(By.XPATH, ".//a[@class='a-link-normal']").get_attribute("href")
        links.append(link)
    return links


def get_product_details(driver, url):

    driver.get(url)
    time.sleep(2)
    product_title = driver.find_element(By.XPATH, "//*[@id='productTitle']").text
    price = driver.find_element(By.XPATH, "//*[@class='a-section a-spacing-none aok-align-center aok-relative']").text
    brand = driver.find_element(By.XPATH, "(//*[@class='a-size-medium a-text-bold'])[3]").text
    return product_title, price, brand


def test_extract_product_details(driver, product_links):
    # Extract details for first 6 products
    product_data = []
    for url in product_links[:6]:  # Limit to first 6 products
        title, price, brand = get_product_details(driver, url)
        product_data.append([title, price, brand])

    # Print the product data in tabular format
    headers = ["Product Title", "Price", "Brand"]
    print("\nProduct Details:")
    print(tabulate.tabulate(product_data, headers=headers, tablefmt="grid"))

    # Assert to ensure data is extracted
    assert len(product_data) == 6, "Not all product details were extracted."
