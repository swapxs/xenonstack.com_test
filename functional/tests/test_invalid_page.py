import logging
import pytest
from helpers.page_loader import page_loader

logger = logging.getLogger(__name__)

@pytest.mark.invalid_page
def test_invalid_page(driver, wait):
    logger.info("Checking 404 Error Handling")

    driver.get("https://xenonstack.com/this-page-does-not-exist")
    page_loader(driver, wait)

    title = driver.title.lower()
    src = driver.page_source.lower()

    if "404" in title or "not found" in src:
        logger.info("404 page correctly displayed.")
        assert True
    else:
        logger.error("404 page is missing or incorrect!")
        assert False, "404 page is missing or incorrect!"
