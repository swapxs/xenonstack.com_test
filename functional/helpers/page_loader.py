import logging
from selenium.common.exceptions import TimeoutException as TE

logger = logging.getLogger(__name__)

def page_loader(driver, wait):
    try:
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        logger.info("Page loaded successfully.")

    except TE:
        logger.warning("Page took too long to load. Stopping load manually.")
        driver.execute_script("window.stop();")
