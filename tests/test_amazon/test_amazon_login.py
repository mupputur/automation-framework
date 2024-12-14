#Open the amazon webpage and print the number of slides and their text
import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


@pytest.fixture(scope="function")
def driver():
    # Path to ChromeDriver
    s = Service(executable_path="C:\\Users\\DELL\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe")
    driver = webdriver.Chrome(service=s)
    driver.maximize_window()
    yield driver
    driver.quit()

def test_amazon_login(driver):

    # Open Amazon website
    driver.get("https://www.amazon.in")
    time.sleep(3)  # Wait for the page to load

    #find_elements to get all elements with the specified class
    slides = driver.find_elements(By.XPATH, "//*[@class='a-carousel-card' and contains (@role,'listitem')]//img")

    print(f"Number of slides found: {len(slides)}")


    # Print and assert details of each slide
    for slide in slides:
        slide_text = slide.get_attribute("alt")
        print("Slide:",slide_text)
        time.sleep(2)

    assert len(slides) > 0, "No slides found on the page"


