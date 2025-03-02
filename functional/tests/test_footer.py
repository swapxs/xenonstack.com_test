from selenium.webdriver.common.by import By
from utils.rich_config import printc
from utils.selenium_config import DRIVER
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


def test_footer():
    printc("\n[head]Test 2.2:[/head]",
           "Ensuring All Footer Links Are Checked Without Skips.")

    DRIVER.get("https://xenonstack.com/")
    page_loader()

    links = extract_links("footer")

    if not links:
        printc("[bug][ x ][/bug] FOOTER TEST FAILED -",
               "No links found in the footer!")
        return

    total_links = len(links)
    printc(f"[info]Total Footer Links Found: {total_links}")
    idx = 0

    while idx < total_links:
        retries = 2
        while retries > 0:
            try:
                links = extract_links("footer")
                if idx >= len(links):
                    printc(
                        "[warn][ - ][/warn] Skipping missing link at index",
                        idx
                    )

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
                    printc(f"[bug][ x ][/bug] Skipping '{link_text}' -",
                           "No href attribute.")
                    break
                printc("[counter][ ! ][/counter] ",
                       f"[counter][{idx + 1}/{total_links}][/counter]",
                       f"Checking Footer Link: {href} -> {link_text}")

                if "xenonstack.com" not in href.lower():
                    check_external_link(href, link_text)

                else:
                    check_internal_link(link, link_text, DRIVER.current_url)

                break

            except SER:
                retries -= 1
                printc("[warn][ - ][/warn] Stale element error. Retrying...")

        idx += 1
    printc("[success][ + ][/success] Footer Test Completed")

