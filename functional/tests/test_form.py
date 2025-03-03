import os
import sys
import time
import logging
import pytest
from selenium.webdriver.common.by import By
from helpers.page_loader import page_loader
from helpers.form_handler import fill_xenon_form

logger = logging.getLogger(__name__)

def check_validation_messages(driver):
    try:
        errors = driver.find_elements(By.CLASS_NAME, "error-message")
        return any(error.is_displayed() for error in errors)

    except Exception:
        return False


@pytest.mark.required_fields
def test_required_field(driver, wait):
    logger.info("Testing For Required Fields.")

    try:
        driver.get("https://xenonstack.com/")
        page_loader(driver, wait)

        logger.info("Clicking 'Get Started' button.")
        driver.find_element(By.CLASS_NAME, "nav-button").click()
        time.sleep(1)

        logger.info("Clicking 'Proceed Next' button without filling form.")
        driver.find_element(By.XPATH, "//p[normalize-space()='Proceed Next']").click()
        time.sleep(1)

        if check_validation_messages(driver):
            logger.info("Required field validation test passed.")
            assert True
        else:
            logger.error("Error message did not appear. Test failed.")
            assert False, "Error message did not appear."

    except Exception:
        exc_type, _, exc_tb = sys.exc_info()
        if exc_tb is not None:
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error(f"Exception occurred: {exc_type}, {fname}, line {exc_tb.tb_lineno}")
            assert False, "Exception encountered in test_required_field"


@pytest.mark.invalid_input
def test_invalid_inputs(driver, wait):
    logger.info("Testing For Invalid Inputs.")

    try:
        driver.get("https://xenonstack.com/")
        page_loader(driver, wait)

        logger.info("Clicking 'Get Started' button.")
        driver.find_element(By.CLASS_NAME, "nav-button").click()
        time.sleep(1)

        fname = "John123"
        lname = "Doe@#"
        email = "invalidemail"
        num = "abcd1234"
        cmpny = "Null Company"

        fill_xenon_form(driver, fname, lname, email, num, cmpny)

        logger.info("Clicking 'Proceed Next' button with invalid inputs.")
        driver.find_element(By.XPATH, "//p[normalize-space()='Proceed Next']").click()
        time.sleep(1)

        if check_validation_messages(driver):
            logger.info("Input validation test passed.")
            assert True
        else:
            logger.error("Error message did not appear. Test failed.")
            assert False, "Error message did not appear."

    except Exception:
        exc_type, _, exc_tb = sys.exc_info()
        if exc_tb is not None:
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error(f"Exception occurred: {exc_type}, {fname}, line {exc_tb.tb_lineno}")
            assert False, "Exception encountered in test_invalid_inputs"


@pytest.mark.valid_input
def test_valid_inputs(driver, wait):
    logger.info("Testing For Valid Inputs.")

    try:
        driver.get("https://xenonstack.com/")
        page_loader(driver, wait)

        logger.info("Clicking 'Get Started' button.")
        driver.find_element(By.CLASS_NAME, "nav-button").click()
        time.sleep(1)

        fname = "Jack"
        lname = "Doe"
        email = "nucmpny@gmail.com"
        num = "05987654312"
        cmpny = "Testify"

        fill_xenon_form(driver, fname, lname, email, num, cmpny)

        logger.info("Clicking 'Proceed Next' button with valid inputs.")
        driver.find_element(By.XPATH, "//p[normalize-space()='Proceed Next']").click()

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
            driver.find_element(By.XPATH, opt_xp).click()

        time.sleep(1)
        if check_validation_messages(driver):
            logger.error("Valid input test failed. Unexpected validation messages detected.")
            assert False, "Form validation failed with valid inputs."
        else:
            logger.info("Valid input test passed. No errors detected.")
            assert True

    except Exception:
        exc_type, _, exc_tb = sys.exc_info()
        if exc_tb is not None:
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error(f"Exception occurred: {exc_type}, {fname}, line {exc_tb.tb_lineno}")
            assert False, "Exception encountered in test_valid_inputs"
