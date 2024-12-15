import selenium
import pytest
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import json

details = []


def test_read_json():

    with open('user_config.json') as output:
        data = json.load(output)
        #print(data["credentials"])
        x = data["credentials"]

    for i in x:
        cred = (i["username"],i["password"])
        #print(details)
        details.append(cred)
        return details

    print(details)



@pytest.mark.parametrize("username,password",details)
def test_instagram(username,password):
    global driver
    driver = webdriver.Chrome(executable_path = "C:\\Users\\jagad\\Desktop\\automation_framework\dependencies\\drivers\\chrome\\chromedriver.exe")
    driver.get("https://www.instagram.com/")
    driver.maximize_window()
    time.sleep(4)
    driver.find_element(By.XPATH,"//input[@name='username']").send_keys(username)
    time.sleep(4)
    driver.find_element(By.NAME,"password").send_keys(password)
    time.sleep(4)
    driver.find_element(By.XPATH,"//div[text()='Log In']").click()
    time.sleep(4)
    assert driver.title == "Instagram"
    









