# /functional/helpers/link_handlers.py
import logging
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from helpers.page_loader import page_loader
from selenium.common.exceptions import TimeoutException as TE, NoSuchElementException as NSE

logger = logging.getLogger(__name__)

def extract_links(driver, wait, html_tag):
    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, html_tag)))
        section = driver.find_element(By.TAG_NAME, html_tag)
        return section.find_elements(By.TAG_NAME, "a")

    except NSE:
        logger.warning(f"No links found in <{html_tag}> section.")
        return []

    except TE:
            logger.error(f"Timeout waiting for <{html_tag}> section.")
            return []


def check_external_link(href, link_text):
    try:
        resp = requests.get(href, timeout=3, stream=True)

        if resp.status_code in [400, 401, 999]:
            logger.warning(f"{link_text} blocks bot requests ({resp.status_code}) or is not available. Marking as valid.")
            return

        elif resp.status_code < 400:
            logger.info(f"External link '{link_text}' is valid. [HTTP {resp.status_code}]")

        else:
            logger.error(f"External link '{link_text}' returned HTTP {resp.status_code}. Possible broken link.")

    except requests.RequestException as e:
        logger.error(f"Failed request for '{link_text}': {str(e)}")


def check_internal_link(driver, wait, link, link_text, old_url) -> bool:
    """Returns True on success, False on error/timeout."""
    try:
        if link.get_attribute("target") == "_blank":
            original_handles = driver.window_handles
            driver.execute_script("window.open(arguments[0]);", link.get_attribute("href"))
            wait.until(EC.new_window_is_opened(original_handles))

            all_handles = driver.window_handles
            if len(all_handles) > len(original_handles):
                driver.switch_to.window(all_handles[-1])
                page_loader(driver, wait)
                new_url = driver.current_url

                if new_url != old_url and new_url != "data:,":
                    logger.info(f"'{link_text}' opened in new tab successfully -> {new_url}")
                else:
                    logger.warning(f"'{link_text}' new tab did not navigate properly.")
                    driver.close()
                    driver.switch_to.window(original_handles[0])
                    return False

                driver.close()
                driver.switch_to.window(original_handles[0])
            else:
                logger.warning(f"No new tab detected for '{link_text}'.")
                return False

        else:
            driver.execute_script("arguments[0].click();", link)
            page_loader(driver, wait)
            wait.until(EC.url_changes(old_url))
            new_url = driver.current_url

            if new_url != old_url and new_url != "data:,":
                logger.info(f"'{link_text}' link works -> navigated to {new_url}")
            else:
                logger.warning(f"'{link_text}' did not navigate properly.")
                return False

            driver.back()
            page_loader(driver, wait)
            wait.until(EC.url_to_be(old_url))

        return True  # Success

    except TE:
        logger.warning(f"Timeout opening link '{link_text}'. Skipping this link.")
        try:
            driver.execute_script("window.stop();")
            driver.back()
            page_loader(driver, wait)
        except Exception as stop_ex:
            logger.warning(f"Couldn't stop page load for '{link_text}'. Reason: {stop_ex}")

        return False

    except Exception as e:
        logger.warning(f"Error opening '{link_text}': {e}")
        try:
            driver.execute_script("window.stop();")
        except Exception as stop_ex:
            logger.warning(f"Couldn't stop page load for '{link_text}'. Reason: {stop_ex}")
        return False
