# /functional/tests/test_load_speed.py
import logging
import pytest
import time
from helpers.page_loader import page_loader
from helpers.link_handlers import extract_links
from selenium.common.exceptions import TimeoutException as TE

# Configure logger
logger = logging.getLogger(__name__)

@pytest.mark.load_speed
def test_load_speed(driver, wait):
    logger.info("Checking Performance of the website")
    driver.get("https://www.xenonstack.com/")
    driver.set_page_load_timeout(60)
    page_loader(driver, wait)

    links = extract_links(driver, wait, "body")
    pages = set()

    for link in links:
        href = link.get_attribute("href")

        if href and "xenonstack.com" in href:
            pages.add(href)

    logger.warning(f"Total Internal Pages Found: {len(pages)}")

    failures = []  # Track test failures

    for page in pages:
        driver.get(page)
        try:
            wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
            try:
                start_time = driver.execute_script(
                    "return window.performance.timing.navigationStart;"
                )
                end_time = driver.execute_script(
                    "return window.performance.timing.loadEventEnd"
                )
                load_time = (end_time - start_time) / 1000

            except Exception:
                load_time = -1

            if load_time > 4:
                msg = f"WARNING: {page} is slow (>4s). Stopping load and going back."
                logger.warning(msg)
                failures.append(msg)
                driver.execute_script("window.stop();")
                driver.back()
                page_loader(driver, wait)

            else:
                logger.info(f"{page} loaded in {load_time}s")

        except TE:
            msg = f"ERROR: {page} failed to load after retries."
            logger.error(msg)
            failures.append(msg)
            driver.execute_script("window.stop();")
            driver.back()
            page_loader(driver, wait)
            continue

    if failures:
        assert False, "Load speed test encountered errors multiple errors"

    logger.info("LOAD SPEED TEST PASSED - No critical issues found.")
    assert True
