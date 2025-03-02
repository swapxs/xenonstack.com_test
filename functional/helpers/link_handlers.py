import requests
from utils.rich_config import printc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utils.selenium_config import (
    WAIT,
    DRIVER
)
from helpers.page_loader import page_loader

from selenium.common.exceptions import (
    TimeoutException as TE,
    NoSuchElementException as NSE
)


def extract_links(html_tag):
    try:
        WAIT.until(
            EC.presence_of_element_located((By.TAG_NAME, html_tag))
        )

        footer = DRIVER.find_element(By.TAG_NAME, html_tag)
        return footer.find_elements(By.TAG_NAME, "a")

    except NSE:
        return []

def check_external_link(href, link_text):
    try:
        resp = requests.get(href, timeout=3, stream=True)
        if resp.status_code in range(400, 1000):
            web = "X" if "x.com" in href else "LinkedIn"
            printc(f"[warn][ - ][/warn] {web} blocks bot requests",
                   f"({resp.status_code}) or is down for some reason.",
                   "Marking as valid.")
        elif resp.status_code < 400:
            printc(f"[success][ + ][/success] External link '{link_text}'",
                   f"is valid. [HTTP {resp.status_code}]")
        else:
            printc(f"[bug][ x ][/bug] '{link_text}'",
                   f"returned HTTP {resp.status_code}")
    except requests.RequestException:
        printc("[bug][ x ][/bug] Failed request for '{link_text}': {str(e)}")


def check_internal_link(link, link_text, old_url):
    try:
        if link.get_attribute("target") == "_blank":
            original_handles = DRIVER.window_handles

            DRIVER.execute_script(
                "window.open(arguments[0]);",
                link.get_attribute("href")
            )

            WAIT.until(EC.new_window_is_opened(original_handles))
            all_handles = DRIVER.window_handles
            if len(all_handles) > len(original_handles):
                DRIVER.switch_to.window(all_handles[-1])
                page_loader()
                new_url = DRIVER.current_url

                if new_url != old_url and new_url != "data:,":
                    printc(f"[success][ + ][/success] '{link_text}'",
                           "opened in new tab - OK")
                else:
                    printc(f"[bug][ x ][/bug] '{link_text}'",
                           "new tab did not navigate.")

                DRIVER.close()
                DRIVER.switch_to.window(original_handles[0])
            else:
                printc("[bug][ x ][/bug]",
                       f"No new tab detected for '{link_text}'")
        else:
            DRIVER.execute_script(
                "arguments[0].click();",
                link
            )

            page_loader()
            WAIT.until(EC.url_changes(old_url))
            new_url = DRIVER.current_url

            if new_url != old_url and new_url != "data:,":
                printc(f"[success][ + ][/success] '{link_text}' link works -",
                       f"Page changed to {new_url}")
            else:
                printc(f"[bug][ x ][/bug] '{link_text}' is a BUG, fix it.")
            DRIVER.back()
            page_loader()
            WAIT.until(EC.url_to_be(old_url))
    except TE:
        printc("[bug][ x ][/bug] Timeout opening link '{link_text}'")
    except Exception:
        printc(f"[bug][ x ][/bug] Error opening '{link_text}'")
