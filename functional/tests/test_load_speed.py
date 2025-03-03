from utils.rich_config import printc
from helpers.page_loader import page_loader
from helpers.link_handlers import extract_links
from selenium.common.exceptions import TimeoutException as TE
from utils.selenium_config import (
    WAIT,
    DRIVER
)


def test_load_speed():
    printc("\n[head]Test 4.1: [/head] Checking Performance of the website")
    DRIVER.get("https://xenonstack.com/")
    page_loader()

    links = extract_links("body")

    pages = set()

    for link in links:
        href = link.get_attribute("href")

        if href and "xenonstack.com" in href:
            pages.add(href)

    printc(f"[info]Total Internal Pages Found: [/info] {len(pages)}")

    for page in pages:
        DRIVER.get(page)
        try:
            WAIT.until(
                lambda d:
                    d.execute_script(
                        "return document.readyState"
                    ) == "complete"
            )

            try:
                start_time = DRIVER.execute_script(
                    "return window.performance.timing.navigationStart;"
                )

                end_time = DRIVER.execute_script(
                    "return window.performance.timing.loadEventEnd"
                )

                load_time = (end_time - start_time) / 1000

            except Exception:
                load_time = -1

            if load_time > 4:
                printc("[bug][ - ][/bug]",
                       f"{page} took {load_time:.2f}s to load.",
                       "[bug]Potential Performance Issue![/bug]")
            else:
                printc("[counter][ + ][/counter]",
                       f"{page} loaded in {load_time:.2f}s")

        except TE:
            printc(f"[bug][ x ][/bug] {page}",
                   "failed to load within the expected time.")
