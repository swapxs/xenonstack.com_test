import os
import sys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from utils.rich_config import printc
from utils.selenium_config import DRIVER
from helpers.page_loader import page_loader
from helpers.form_handler import injkt


def detect_vuln():
    try:
        txt = Alert(DRIVER).text
        Alert(DRIVER).dismiss()
        printc(f"[bug][ x ][/bug] XSS Alert Detected! Message: {txt}")
        return True
    except Exception:
        return False


def test_injection_SQL():
    printc("\n[head]Test 2.1: [/head]"
           " Testing For SQL Injection.")
    try:
        DRIVER.get("https://xenonstack.com/")
        page_loader()

        printc("[bold yellow][ * ][/bold yellow] Get Started Button Clicked")
        DRIVER.find_element(By.CLASS_NAME, "nav-button").click()
        time.sleep(1)

        injkt("' OR '1'='1'; --")

        printc("[bold yellow][ * ][/bold yellow] Proceed Next Button Clicked")
        DRIVER.find_element(By.XPATH,
                            "//p[normalize-space()='Proceed Next']"
                            ).click()

        page_source = DRIVER.page_source.lower()
        if "error" not in page_source and "invalid" not in page_source:
            printc("[bug][ x ][/bug] Vulnerability Detected")

        else:
            printc("[success][ + ][/success]"
                   " SQL Injection Detection Test Passed")

    except Exception:
        exc_type, _, exc_tb = sys.exc_info()
        if exc_tb is not None:
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            printc("[bug][ x ][/bug]",
                   exc_type, fname, exc_tb.tb_lineno)


def test_injection_XSS():
    printc("\n[head]Test 2.2: [/head]"
           " Testing For Script Injection or Cross Site Scripting (XSS)")
    try:
        DRIVER.get("https://xenonstack.com/")
        page_loader()

        printc("[bold yellow][ * ][/bold yellow] Get Started Button Clicked")
        DRIVER.find_element(By.CLASS_NAME, "nav-button").click()
        time.sleep(1)

        injkt("<script>alert('Vulnerabile to XSS')</script>")

        printc("[bold yellow][ * ][/bold yellow] Proceed Next Button Clicked")
        DRIVER.find_element(By.XPATH,
                            "//p[normalize-space()='Proceed Next']"
                            ).click()

        if detect_vuln():
            printc("[bug][ x ][/bug] Vulnerability Detected")

        else:
            printc("[success][ + ][/success]"
                   " XSS Injection Detection Test Passed")

    except Exception:
        exc_type, _, exc_tb = sys.exc_info()
        if exc_tb is not None:
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            printc("[bug][ x ][/bug]",
                   exc_type, fname, exc_tb.tb_lineno)
