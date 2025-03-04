# /functional/tests/test_footer.py
import logging
import pytest
from selenium.webdriver.common.by import By
from helpers.page_loader import page_loader
from helpers.link_handlers import (
    extract_links,
    check_external_link,
    check_internal_link
)

from selenium.common.exceptions import (
    StaleElementReferenceException as SER,
    NoSuchElementException as NSE
)

logger = logging.getLogger(__name__)

@pytest.mark.footer
def test_footer(driver, wait):
    logger.info("Ensuring All Footer Links Are Checked Without Skips.")

    driver.get("https://xenonstack.com/")
    page_loader(driver, wait)

    links = extract_links(driver, wait, "footer")
    if not links:
        logger.error("FOOTER TEST FAILED - No links found in the footer!")
        assert False, "No footer links found."

    total_links = len(links)
    logger.info(f"Total Footer Links Found: {total_links}")
    idx = 0

    failed = []
    while idx < total_links:
        retries = 2
        while retries > 0:
            try:
                links = extract_links(driver, wait, "footer")
                if idx >= len(links):
                    logger.warning(f"Skipping missing links")
                    break

                link = links[idx]
                link_text = link.text.strip()
                href = link.get_attribute("href")

                if not link_text:
                    try:
                        img = link.find_element(By.TAG_NAME, "img")
                        alt_text = img.get_attribute("alt")
                        if alt_text:
                            link_text = alt_text.strip()
                    except NSE:
                        pass
                    if not link_text:
                        link_text = "N/A"

                if not href:
                    msg = f"Skipping '{link_text}' - No href attribute."
                    logger.error(msg)
                    failed.append(msg)
                    break

                logger.info(f"Checking Footer Link {idx + 1}/{total_links}: {href} -> {link_text}")

                if "xenonstack.com" not in href.lower():
                    check_external_link(href, link_text)
                else:
                    if not check_internal_link(driver, wait, link, link_text, driver.current_url):
                        msg = f"BUG: '{link_text}' link did not navigate correctly."
                        logger.error(msg)
                        failed.append(msg)
                break

            except SER:
                retries -= 1
                msg = "Stale element error. Retrying..."
                logger.warning(msg)
                failed.append(msg)

        idx += 1

    if failed:
        assert False, "Some footer links dont work as intended"

    logger.info("Footer Test Completed Successfully.")
    assert True
