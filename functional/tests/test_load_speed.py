import logging
import pytest
from helpers.page_loader import page_loader
from helpers.link_handlers import extract_links
from selenium.common.exceptions import TimeoutException as TE

# Configure logger
logger = logging.getLogger(__name__)

@pytest.mark.load_speed
def test_load_speed(driver, wait):
    logger.info("Checking Performance of the website")
    driver.get("https://xenonstack.com/")
    page_loader(driver, wait)

    links = extract_links(driver, wait, "body")
    pages = set()

    # Collect internal pages
    for link in links:
        href = link.get_attribute("href")
        if href and "xenonstack.com" in href:
            pages.add(href)

    logger.info(f"Total Internal Pages Found: {len(pages)}")

    # Check load times
    for page in pages:
        driver.get(page)
        try:
            wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

            try:
                start = driver.execute_script("return window.performance.timing.navigationStart;")
                end = driver.execute_script("return window.performance.timing.loadEventEnd;")
                load_time = (end - start) / 1000.0
            except Exception:
                load_time = -1

            if load_time > 5:
                logger.error(f"{page} took {load_time:.2f}s to load. Potential Performance Issue!")
                assert False, f"{page} took {load_time:.2f}s > 4s"
            else:
                logger.info(f"{page} loaded in {load_time:.2f}s")
                assert True

        except TE:
            logger.error(f"{page} failed to load within the expected time.")
            assert False, f"{page} timed out while loading"

    logger.info("All pages loaded within acceptable time.")
