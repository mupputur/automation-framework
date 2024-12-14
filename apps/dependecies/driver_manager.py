from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time


class DriverManager:

    def __init__(self):
        self.driver = None
        self.url = "https://www.lawsonproducts.com/"
        self.initialize_driver()

    def initialize_driver(self):
        try:
            service = Service(executable_path='..\\dependecies\\chromedriver.exe')
            self.driver = webdriver.Chrome(service=service)
            self.driver.maximize_window()
            self.driver.get(self.url)
        except Exception as e:
            print(f"Error: {str(e)}")
            raise Exception("Failed to initialize driver or Unable to launch the app")

# The below lines are to test this module
# this won't run when we import this module into another file
if __name__ == "__main__":
    driver = DriverManager()
    time.sleep(3)
