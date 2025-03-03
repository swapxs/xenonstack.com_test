import time
from selenium.webdriver.common.by import By
from utils.rich_config import printc
from utils.selenium_config import DRIVER
from helpers.page_loader import page_loader
from helpers.item_handlers import get_nav_items
from selenium.common.exceptions import (
    TimeoutException as TE,
    StaleElementReferenceException as SER,
    NoSuchElementException as NSE
)


def test_navbar():
    printc("\n[head]Test 3.1: [/head]"
           " Testing The Navigation Bar In The Website")
    try:
        DRIVER.get("https://xenonstack.com/")
        page_loader()

        nav_items = get_nav_items()

        if not nav_items:
            printc("[bug][ x ][/bug]"
                   "NAVBAR DOES NOT WORK - No navbar items found!")
            return

        printc("[info]Available Navbar Items: [/info]",
               [el.text for el in nav_items])

        for link_text in [
            el.text.strip() for el in nav_items if el.text.strip()
        ]:
            try:
                old_url = DRIVER.current_url
                nav_items = get_nav_items()
                item = next(
                    (el for el in nav_items if el.text.strip() == link_text),
                    None
                )

                if not item:
                    printc("[bug][ x ][/bug]"
                           " [alrt]BUG:[/alrt] NAVBAR DOES NOT WORK - ",
                           link_text, " missing after reload")
                    continue

                try:
                    link = item.find_element(By.TAG_NAME, "a")
                    href = link.get_attribute("href")

                    if href:
                        printc("[bold bright_yellow][ ! ][/bold bright_yellow]"
                               " Clicking direct link: ", href)

                        DRIVER.execute_script("arguments[0].click();", link)
                    else:
                        printc("[bug][ x ][/bug]"
                               " No href found for ", link_text,
                               " trying JavaScript click.")

                        DRIVER.execute_script("arguments[0].click();", item)

                except NSE:
                    printc("[bug][ x ][/bug]"
                           " [alrt]BUG:[/alrt] No <a> tag found for ",
                           link_text, ". Using JavaScript click.")

                    DRIVER.execute_script("arguments[0].click();", item)

                time.sleep(1)
                new_url = DRIVER.current_url

                if new_url != old_url and new_url != "data:,":
                    printc("[success][ + ][/success]"
                           " ", link_text, " works - Page changed")
                else:
                    printc("[bug][ x ][/bug]"
                           " [alrt]BUG:[/alrt]",
                           link_text, " did nothing or redirected to data:,")

                DRIVER.forward()
                time.sleep(1)

            except SER:
                printc("[bug][ x ][/bug]"
                       " [alrt]BUG:[/alrt] Stale element error for ",
                       link_text)

            except TE:
                printc("[bug][ x ][/bug]"
                       " [alrt]BUG:[/alrt] Timeout waiting for ",
                       link_text)

            except Exception:
                printc("[bug][ x ][/bug]"
                       " [alrt]BUG:[/alrt] NAVBAR DOES NOT WORK")

        printc("[success][ + ][/success]"
               " Navbar Test Completed")

    except Exception:
        printc("[bug][ x ][/bug]"
               " [alrt]BUG:[/alrt] NAVBAR DOES NOT WORK")
