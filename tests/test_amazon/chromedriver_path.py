import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


# This fixture reads the --driver option to select the WebDriver
@pytest.fixture(scope="module")
def driver():
    s = Service(executable_path="C:\\Users\\DELL\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe")
    driver = webdriver.Chrome(service=s)
    driver.maximize_window()
    yield driver
    driver.quit()
