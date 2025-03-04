# /functional/tests/test_navbar.py
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
        driver.get("https://www.xenonstack.com/")
        page_loader(driver, wait)

        nav_items = get_nav_items(driver, wait)

        if not nav_items:
            msg = "NAVBAR TEST FAILED - No navbar items found!"
            logger.error(msg)
            failures.append(msg)

        else:
            logger.info(f"Available Navbar Items: {[el.text for el in nav_items]}")

            for item in nav_items:

                link_text = ""
                try:
                    link_text = item.text.strip()
                    if not link_text:
                        continue

                    # Extract 'onclick' attribute
                    onclick_attr = item.get_attribute("onclick")
                    if not onclick_attr or "scrollToSection" not in onclick_attr:
                        logger.warning(f"Skipping '{link_text}' - No scroll function detected.")
                        continue
                    
                    # Extract section ID from onclick="scrollToSection('section-id')"
                    section_id = onclick_attr.split("'")[1]  # Extract ID inside single quotes
                    logger.info(f"Navbar item '{link_text}' maps to section '{section_id}'.")

                    # Store initial scroll position
                    start_scroll = driver.execute_script("return window.scrollY;")

                    # Click on the navbar item
                    driver.execute_script("arguments[0].click();", item)
                    time.sleep(2)  # Allow scrolling time

                    # Check if the correct section is in view
                    target_element = driver.find_element(By.ID, section_id)
                    is_visible = driver.execute_script(
                        "var rect = arguments[0].getBoundingClientRect();"
                        "return (rect.top >= 0 && rect.bottom <= window.innerHeight);",
                        target_element
                    )

                    end_scroll = driver.execute_script("return window.scrollY;")

                    if is_visible or end_scroll != start_scroll:
                        logger.info(f"'{link_text}' scrolled to '{section_id}' correctly.")
                    else:
                        msg = f"'{link_text}' did not scroll to '{section_id}' properly."
                        logger.warning(msg)
                        failures.append(msg)

                except NSE:
                    msg = f"FAILED - No element found for '{link_text}'."
                    logger.error(msg)
                    failures.append(msg)

                except SER:
                    msg = f"FAILED - Stale element reference for '{link_text}'. Retrying."
                    logger.warning(msg)
                    failures.append(msg)

                except TE:
                    msg = f"FAILED - Timeout while waiting for '{link_text}'."
                    logger.error(msg)
                    failures.append(msg)

                except Exception as e:
                    msg = f"FAILED - Error on '{link_text}': {e}"
                    logger.error(msg)
                    failures.append(msg)

        logger.info("Navbar Test Completed.")

    except Exception as e:
        msg = f"NAVBAR TEST FAILED - Caught exception: {e}"
        logger.error(msg)
        failures.append(msg)

    if failures:
        assert False, "Navbar Does not work as intended"
    else:
        logger.info("Navbar test completed successfully.")
        assert True
