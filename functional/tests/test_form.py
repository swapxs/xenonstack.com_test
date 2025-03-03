import os
import sys
import time
from selenium.webdriver.common.by import By
from utils.rich_config import printc
from utils.selenium_config import DRIVER
from helpers.page_loader import page_loader
from helpers.form_handler import fill_xenon_form


def check_validation_messages():
    try:
        errors = DRIVER.find_elements(By.CLASS_NAME, "error-message")
        return any(error.is_displayed() for error in errors)
    except Exception:
        return False


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
        time.sleep(1)

        if check_validation_messages():
            printc("[success][ + ][/success]"
                   " Required Filed Validation Test",
                   "[success]Passed[/success]."
                   " It does not let us go through without entering data.")
        else:
            printc("[bug][ x ][/bug]"
                   " Error message did not appear."
                   " Test [bug]Failed[/bug]")

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

        time.sleep(1)
        if check_validation_messages():
            printc("[success][ + ][/success]"
                   " Input Validation Testing ",
                   "[success]Passed[/success].",
                   " Does not let us go through without providing proper",
                   "inputs.")
        else:
            printc("[bug][ x ][/bug]"
                   " Error message did not appear."
                   " Test [bug]Failed[/bug]")

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

        time.sleep(1)
        if check_validation_messages():
            printc("[bug][ x ][/bug] Valid input test failed. Unexpected error"
                   "messages detected!")
        else:
            printc("[success][ + ][/success] Valid input test passed."
                   "No errors detected.")

    except Exception:
        exc_type, _, exc_tb = sys.exc_info()
        if exc_tb is not None:
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            printc("[bug][ x ][/bug]",
                   exc_type, fname, exc_tb.tb_lineno)
