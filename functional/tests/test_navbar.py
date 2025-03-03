import time
import logging
import pytest
from selenium.webdriver.common.by import By
from helpers.page_loader import page_loader
from helpers.item_handlers import get_nav_items
from selenium.common.exceptions import (
    TimeoutException as TE,
    StaleElementReferenceException as SER,
    NoSuchElementException as NSE
)

logger = logging.getLogger(__name__)

@pytest.mark.navbar
def test_navbar(driver, wait):
    logger.info("Testing The Navigation Bar In The Website")

    failures = []

    try:
        driver.get("https://xenonstack.com/")
        page_loader(driver, wait)

        nav_items = get_nav_items(driver, wait)

        if not nav_items:
            msg = "NAVBAR DOES NOT WORK - No navbar items found!"
            logger.error(msg)
            failures.append(msg)

        else:
            logger.info(f"Available Navbar Items: {[el.text for el in nav_items]}")

            for link_text in [el.text.strip() for el in nav_items if el.text.strip()]:
                try:
                    old_url = driver.current_url
                    nav_items = get_nav_items(driver, wait)
                    item = next((el for el in nav_items if el.text.strip() == link_text), None)

                    if not item:
                        msg = f"NAVBAR DOES NOT WORK - item '{link_text}' missing after reload."
                        logger.error(msg)
                        failures.append(msg)
                        continue

                    try:
                        link = item.find_element(By.TAG_NAME, "a")
                        href = link.get_attribute("href")

                        if href:
                            logger.info(f"Clicking direct link: {href}")
                            driver.execute_script("arguments[0].click();", link)
                        else:
                            msg = f"No href found for '{link_text}', trying JavaScript click."
                            logger.warning(msg)
                            failures.append(msg)
                            driver.execute_script("arguments[0].click();", item)

                    except NSE:
                        msg = f"No <a> tag found for '{link_text}', using JavaScript click."
                        logger.warning(msg)
                        failures.append(msg)
                        driver.execute_script("arguments[0].click();", item)

                    time.sleep(1)
                    new_url = driver.current_url

                    if new_url != old_url and new_url != "data:,":
                        logger.info(f"'{link_text}' works - Page changed.")
                    else:
                        msg = f"'{link_text}' did nothing or redirected to data:, old_url={old_url}, new_url={new_url}"
                        logger.error(msg)
                        failures.append(msg)

                    driver.forward()
                    time.sleep(1)

                except SER:
                    msg = f"Stale element error for '{link_text}'"
                    logger.warning(msg)
                    failures.append(msg)

                except TE:
                    msg = f"Timeout waiting for '{link_text}'"
                    logger.error(msg)
                    failures.append(msg)

                except Exception as e:
                    msg = f"NAVBAR DOES NOT WORK on '{link_text}' - {e}"
                    logger.error(msg)
                    failures.append(msg)

        logger.info("Navbar Test Completed.")

    except Exception as e:
        msg = f"NAVBAR DOES NOT WORK - Caught exception: {e}"
        logger.error(msg)
        failures.append(msg)

    if failures:
        combined = "\n".join(failures)
        assert False, f"Navbar test encountered errors:\n{combined}"
    else:
        logger.info("No critical navbar errors found.")
        assert True
