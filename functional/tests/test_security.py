# /functional/tests/test_security.py
import os
import sys
import time
import logging
import pytest
from selenium.webdriver.common.by import By
from helpers.page_loader import page_loader
from helpers.form_handler import injkt
from helpers.detect_vuln import detect_vuln

logger = logging.getLogger(__name__)

@pytest.mark.injection_SQL
def test_injection_SQL(driver, wait):
    logger.info("Test 2.1: Testing For SQL Injection.")
    try:
        driver.get("https://xenonstack.com/")
        page_loader(driver, wait)

        logger.info("Clicking 'Get Started' button.")
        driver.find_element(By.CLASS_NAME, "nav-button").click()
        time.sleep(1)

        injkt(driver, "' OR '1'='1'; --")

        logger.info("Clicking 'Proceed Next' button.")
        driver.find_element(By.XPATH, "//p[normalize-space()='Proceed Next']").click()

        page_source = driver.page_source.lower()

        if "error" not in page_source and "invalid" not in page_source:
            logger.error("Possible SQL injection vulnerability detected!")
            assert False, "Possible SQL injection vulnerability: no error or invalid message found."
        else:
            logger.info("SQL Injection Detection Test Passed.")
            assert True

    except Exception:
        exc_type, _, exc_tb = sys.exc_info()
        if exc_tb is not None:
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msg = f"Uncaught Exception in test_injection_SQL: {exc_type}, {fname}, line {exc_tb.tb_lineno}"
            logger.error(msg)
            assert False, msg


@pytest.mark.injection_XSS
def test_injection_XSS(driver, wait):
    logger.info("Test 2.2: Testing For Script Injection or Cross-Site Scripting (XSS).")
    try:
        driver.get("https://xenonstack.com/")
        page_loader(driver, wait)

        logger.info("Clicking 'Get Started' button.")
        driver.find_element(By.CLASS_NAME, "nav-button").click()
        time.sleep(1)

        injkt(driver, "<script>alert('Vulnerable to XSS')</script>")

        logger.info("Clicking 'Proceed Next' button.")
        driver.find_element(By.XPATH, "//p[normalize-space()='Proceed Next']").click()

        if detect_vuln(driver):
            logger.error("XSS vulnerability detected!")
            assert False, "XSS vulnerability found (alert was triggered)."
        else:
            logger.info("XSS Injection Detection Test Passed.")
            assert True

    except Exception:
        exc_type, _, exc_tb = sys.exc_info()
        if exc_tb is not None:
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msg = f"Uncaught Exception in test_injection_XSS: {exc_type}, {fname}, line {exc_tb.tb_lineno}"
            logger.error(msg)
            assert False, msg
