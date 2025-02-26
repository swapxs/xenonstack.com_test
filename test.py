import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from rich import print as printc
import time

OPT = Options()
OPT.add_argument("--start-maximized")
OPT.add_argument("--disable-blink-features=AutomationControlled")
OPT.add_argument("--headless=new")  # Run headless

SERVICE = Service("/usr/bin/chromedriver", log_output="/dev/null")
DRIVER = webdriver.Chrome(service=SERVICE, options=OPT)
DRIVER.get("https://www.xenonstack.com/")


def test_required_field():
    try:
        DRIVER.find_element(By.CLASS_NAME, "nav-button").click()
        time.sleep(1)

        DRIVER.find_element(By.XPATH,
                            "//p[normalize-space()='Proceed Next']"
                            ).click()

        err = DRIVER.find_elements(By.CLASS_NAME, "error-message")
        assert len(err) > 0, "Error message did not appear"

        printc("[bold green][ SUCCESS ][/bold green]"
               "Required Filed Validation Test Passed")

    except Exception:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        printc("[bold red][ ERROR ][/bold red]", exc_type, fname, exc_tb.tb_lineno)


def test_invalid_inputs():
    try:
        DRIVER.find_element(By.NAME, "firstname").send_keys("John123")
        DRIVER.find_element(By.NAME, "lastname").send_keys("Doe@#")
        DRIVER.find_element(By.NAME, "email").send_keys("invalidemail")
        DRIVER.find_element(By.NAME, "contact").send_keys("abcd1234")
        DRIVER.find_element(By.NAME, "company").send_keys("Null Company")
        dropdown = Select(DRIVER.find_element(By.ID, "enterpriseIndustry"))
        dropdown.select_by_index(2)

        DRIVER.find_element(By.XPATH,
                            "//p[normalize-space()='Proceed Next']"
                            ).click()

        err = DRIVER.find_elements(By.CLASS_NAME, "error-message")
        assert len(err) > 0, "Invalid inputs were accepted!"

        printc("[bold green][ SUCCESS ][/bold green]"
               " Invalid Input Handling Test Passed")

    except Exception:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        printc("[bold red][ ERROR ][/bold red]", exc_type, fname, exc_tb.tb_lineno)


def test_injection_SQL():
    try:
        payload = "' OR '1'='1'; --"

        DRIVER.find_element(By.NAME, "firstname").send_keys(payload)
        DRIVER.find_element(By.NAME, "lastname").send_keys(payload)
        DRIVER.find_element(By.NAME, "email").send_keys("test.site@corp.com")
        DRIVER.find_element(By.NAME, "contact").send_keys("abcd1234")
        DRIVER.find_element(By.NAME, "company").send_keys("testsite")
        dropdown = Select(DRIVER.find_element(By.ID, "enterpriseIndustry"))
        dropdown.select_by_index(2)

        DRIVER.find_element(By.XPATH,
                            "//p[normalize-space()='Proceed Next']"
                            ).click()

        assert "error" in DRIVER.page_source.lower(), "Vulnerability Detected"

        printc("[bold green][ SUCCESS ][/bold green]"
               " SQL Injection Detection Test Passed")

    except Exception:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        printc("[bold red][ ERROR ][/bold red]", exc_type, fname, exc_tb.tb_lineno)


if __name__ == "__main__":
    test_required_field()
    test_invalid_inputs()
    test_injection_SQL()
    DRIVER.quit()
