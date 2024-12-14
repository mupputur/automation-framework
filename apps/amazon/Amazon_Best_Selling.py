from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import tabulate

# Path to ChromeDriver
s = Service(executable_path="C:\\Users\\DELL\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe")
driver = webdriver.Chrome(service=s)

# Open Amazon website
driver.get("https://www.amazon.in")
driver.maximize_window()
time.sleep(3)

# Navigate to the Best Sellers section in Clothing & Accessories
best_sellers_section = driver.find_element(By.XPATH, "//*[text()='Best Sellers in Clothing & Accessories']")
best_sellers_section.click()
print(best_sellers_section.text)
time.sleep(3)

# Extract product links dynamically from the Best Sellers list
product_elements = driver.find_elements(By.XPATH,"//ul[@class='a-unordered-list a-nostyle a-horizontal feed-carousel-shelf']//li")
product_links = []
for element in product_elements:
    link = element.find_element(By.XPATH, ".//a[@class='a-link-normal']").get_attribute("href")
    product_links.append(link)


# Define a function to extract product details
def get_product_details(url):
    driver.get(url)
    time.sleep(2)

    # Extract product title, price, and brand
    product_title = driver.find_element(By.XPATH, "//*[@id='productTitle']").text
    price = driver.find_element(By.XPATH, "//*[@class='a-section a-spacing-none aok-align-center aok-relative']").text
    brand = driver.find_element(By.XPATH, "(//*[@class='a-size-medium a-text-bold'])[3]").text

    return product_title, price, brand


product_data = []

# Loop through each product link and extract details
for product in product_links[:6]:
    title, price, brand = get_product_details(product)
    product_data.append([title, price, brand])

# Print the extracted data in tabular format
headers = ["Product Title", "Price", "Brand"]
print("\nProduct Details:")
print(tabulate.tabulate(product_data, headers=headers, tablefmt="grid"))

# Close the browser
driver.quit()
