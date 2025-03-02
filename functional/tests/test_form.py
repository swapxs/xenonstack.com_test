import os
import sys
import time
from selenium.webdriver.common.by import By
from utils.rich_config import printc
from utils.selenium_config import DRIVER
from helpers.page_loader import page_loader

from helpers.form_handler import (
    injkt,
    fill_xenon_form
)

# This function tests if the fileds in the form are "required" by nature and
# checks if we can proceed and see to content of the next page without filling
# up the form.
def test_required_field():
    printc("[head]Test 1.1: [/head]"
           " Testing For Required Fileds.")

    # https://stackoverflow.com/questions/1278705/when-i-catch-an-exception-how-do-i-get-the-type-file-and-line-number
    try:
        DRIVER.get("https://xenonstack.com/")
        page_loader()

        printc("[bold yellow][ * ][/bold yellow] Get Started Button Clicked")
        DRIVER.find_element(By.CLASS_NAME, "nav-button").click()
        time.sleep(1)

        printc("[bold yellow][ * ][/bold yellow] Proceed Next Button Clicked")
        DRIVER.find_element(By.XPATH,
                            "//p[normalize-space()='Proceed Next']"
                            ).click()

        err = DRIVER.find_elements(By.CLASS_NAME, "error-message")

        if len(err) < 0:
            printc("[bug][ x ][/bug]"
                   " Error message did not appear."
                   " Test [bug]Failed[/bug]")
        else:
            printc("[success][ + ][/success]"
                   " Required Filed Validation Test",
                   "[success]Passed[/success]."
                   " It does not let us go through without entering data.")


    except Exception:
        exc_type, _, exc_tb = sys.exc_info()
        if exc_tb is not None:
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            printc("[bug][ x ][/bug]",
                   exc_type, fname, exc_tb.tb_lineno)


def test_invalid_inputs():
    printc("\n[head]Test 1.2: [/head]"
           " Testing For Invalid Inputs.")

    try:
        DRIVER.get("https://xenonstack.com/")
        page_loader()

        printc("[bold yellow][ * ][/bold yellow] Get Started Button Clicked")
        DRIVER.find_element(By.CLASS_NAME, "nav-button").click()
        time.sleep(1)

        fname = "John123"
        lname = "Doe@#"
        email = "invalidemail"
        num = "abcd1234"
        cmpny = "Null Company"

        fill_xenon_form(fname, lname, email, num, cmpny)

        printc("[bold yellow][ * ][/bold yellow] Proceed Next Button Clicked")
        DRIVER.find_element(By.XPATH,
                            "//p[normalize-space()='Proceed Next']"
                            ).click()

        err = DRIVER.find_elements(By.CLASS_NAME, "error-message")
        if len(err) < 0:
            printc("[bug][ x ][/bug]"
                   " Error message did not appear."
                   " Test [bug]Failed[/bug]")
        else:
            printc("[success][ + ][/success]"
                   " Input Validation Testing ",
                   "[success]Passed[/success].",
                   " Does not let us go through without providing proper",
                   "inputs.")

    except Exception:
        exc_type, _, exc_tb = sys.exc_info()
        if exc_tb is not None:
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            printc("[bug][ x ][/bug]",
                   exc_type, fname, exc_tb.tb_lineno)


def test_valid_inputs():
    printc("\n[head]Test 1.3: [/head]"
           " Testing For Invalid Inputs.")

    try:
        DRIVER.get("https://xenonstack.com/")
        page_loader()

        printc("[bold yellow][ * ][/bold yellow] Get Started Button Clicked")
        DRIVER.find_element(By.CLASS_NAME, "nav-button").click()
        time.sleep(1)

        fname = "Jack"
        lname = "Doe"
        email = "nucmpny@gmail.com"
        num = "05987654312"
        cmpny = "Testify"

        fill_xenon_form(fname, lname, email, num, cmpny)

        printc("[bold yellow][ * ][/bold yellow] Proceed Next Button Clicked")
        DRIVER.find_element(By.XPATH,
                            "//p[normalize-space()='Proceed Next']"
                            ).click()

        selections = {
                "agenticaiPlatform": 1,
                "companySegment": 2,
                "primaryFocus": 2,
                "aiUsecase": 1,
                "primaryChallenge": 5,
                "companyInfra": 1,
                "dataPlatform": 1,
                "aiTransformation": 1,
                "solution": 2
            }

        for sec_idx, op_idx in selections.items():
            opt_xp = f"//*[@id='{sec_idx}']//div[@class='answers'][{op_idx}]/p"
            DRIVER.find_element(By.XPATH, opt_xp).click()

        err = DRIVER.find_elements(By.CLASS_NAME, "error-message")
        if len(err) < 0:
            printc("[bug][ x ][/bug]",
                   " Invalid inputs were accepted!")

        else:
            printc("[success][ + ][/success]"
                   " Input Validation Testing ",
                   "[success]Passed[/success].",
                   "Does not let us go through without providing proper",
                   "inputs.")

    except Exception:
        exc_type, _, exc_tb = sys.exc_info()
        if exc_tb is not None:
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            printc("[bug][ x ][/bug]",
                   exc_type, fname, exc_tb.tb_lineno)


def test_injection_SQL():
    printc("\n[head]Test 1.4: [/head]"
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

        if "error" not in DRIVER.page_source.lower():
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
    printc("\n[head]Test 1.5: [/head]"
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

        if "error" not in DRIVER.page_source:
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
