import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument("--headless=new")  # Run headless

service = Service("/usr/bin/chromedriver", log_output=None)
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://www.xenonstack.com/")
time.sleep(4)


def test_required_field():
    try:
        driver.find_element(By.CLASS_NAME, "nav-button").click()
        time.sleep(2)

        driver.find_element(By.XPATH,
                            "//p[normalize-space()='Proceed Next']"
                            ).click()
        time.sleep(2)

        errors = driver.find_elements(By.CLASS_NAME, "error-message")
        assert len(errors) > 0, "Error message did not appear"

        print("SUCCESS: Required Filed Validation Test Passed")

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


def test_invalid_inputs():
    try:
        driver.find_element(By.NAME, "firstname").send_keys("John123")
        driver.find_element(By.NAME, "lastname").send_keys("Doe@#")
        driver.find_element(By.NAME, "email").send_keys("invalidemail")
        driver.find_element(By.NAME, "contact").send_keys("abcd1234")
        driver.find_element(By.NAME, "company").send_keys("Null Company")
        dropdown = Select(driver.find_element(By.ID, "enterpriseIndustry"))
        dropdown.select_by_index(2)

        driver.find_element(By.XPATH, "//p[normalize-space()='Proceed Next']").click()
        time.sleep(2)

        errors = driver.find_elements(By.CLASS_NAME, "error-message")
        assert len(errors) > 0, "Invalid inputs were accepted!"

        print("SUCCESS: Invalid Input Handling Test Passed")
        driver.quit()

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


test_required_field()

test_invalid_inputs()
