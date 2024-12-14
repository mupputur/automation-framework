import pytest
from .chromedriver_path import driver
from selenium.webdriver.common.by import By
import time
import tabulate
from .product_items import get_product_details


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

def test_extract_product_details(driver, product_links):
    # Extract details for first 6 products
    max_products_to_fetch = min(6, len(product_links))
    product_data = []
    for url in product_links[:max_products_to_fetch]:
        title, price, brand = get_product_details(driver, url)
        product_data.append([title, price, brand])

    # Print the product data in tabular format
    headers = ["Product Title", "Price", "Brand"]
    print("\nProduct Details:")
    print(tabulate.tabulate(product_data, headers=headers, tablefmt="grid"))

    # Assert to ensure data is extracted
    assert len(product_data) == max_products_to_fetch, "Failed to extract product details for all links."

