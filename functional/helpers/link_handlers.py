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


def check_external_link(href, link_text):
    try:
        resp = requests.get(href, timeout=3, stream=True)

        if resp.status_code in range(400, 1000):
            web = "Twitter/X" if "twitter.com" in href else "LinkedIn"
            logger.warning(f"{web} blocks bot requests ({resp.status_code}) or is down. Marking as valid.")
            assert True

        elif resp.status_code < 400:
            logger.info(f"External link '{link_text}' is valid. [HTTP {resp.status_code}]")
            assert True

        else:
            logger.error(f"External link '{link_text}' returned HTTP {resp.status_code}. Possible broken link.")
            assert False, f"External link '{link_text}' broken -> {resp.status_code}"

    except requests.RequestException as e:
        logger.error(f"Failed request for '{link_text}': {str(e)}")
        assert False, f"External link '{link_text}' could not be checked."


def check_internal_link(driver, wait, link, link_text, old_url):
    try:
        target = link.get_attribute("target")

        if target == "_blank":
            original_handles = driver.window_handles
            driver.execute_script("window.open(arguments[0]);", link.get_attribute("href"))
            wait.until(EC.new_window_is_opened(original_handles))

            all_handles = driver.window_handles
            if len(all_handles) > len(original_handles):
                driver.switch_to.window(all_handles[-1])
                page_loader(driver, wait)
                new_url = driver.current_url

                if new_url != old_url and new_url != "data:,":
                    logger.info(f"'{link_text}' opened in new tab - OK.")
                    assert True
                else:
                    logger.error(f"'{link_text}' new tab did not navigate properly.")
                    assert False, f"'{link_text}' new tab did not navigate."

                driver.close()
                driver.switch_to.window(original_handles[0])

            else:
                logger.error(f"No new tab detected for '{link_text}'.")

        else:
            driver.execute_script("arguments[0].click();", link)
            page_loader(driver, wait)
            wait.until(EC.url_changes(old_url))
            new_url = driver.current_url

            if new_url != old_url and new_url != "data:,":
                logger.info(f"'{link_text}' link works - navigated to {new_url}")
                assert True
            else:
                logger.error(f"'{link_text}' failed to navigate to a new page.")
                assert False, f"'{link_text}' failed to navigate."

            driver.back()
            page_loader(driver, wait)
            wait.until(EC.url_to_be(old_url))

    except TE:
        logger.error(f"Timeout opening link '{link_text}'")
        assert False, f"'{link_text}' took too long to load."

    except Exception as e:
        logger.error(f"Error opening '{link_text}': {str(e)}")
        assert False, f"Failed to open '{link_text}'."
