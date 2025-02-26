import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# https://github.com/Textualize/rich?tab=readme-ov-file
from rich import print as printc
import time

OPT = Options()
OPT.add_argument("--start-maximized")
OPT.add_argument("--disable-blink-features=AutomationControlled")
OPT.add_argument("--headless=new")  # Run headless

SERVICE = Service("/usr/bin/chromedriver", log_output="/dev/null")
DRIVER = webdriver.Chrome(service=SERVICE, options=OPT)
DRIVER.get("https://www.xenonstack.com/")

# ======================
# -- Helper Functions --
# ======================


def wait_for_navbar():
    try:
        WebDriverWait(DRIVER, 1).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                "ul.nav-pointers li.nav-li.item"
            ))
        )

    except TimeoutException:
        printc("[bold bright_red][ ERROR ][/bold bright_red]"
               "Navbar elements did not load in time!")
        return
    return True

# ====================
# -- TESTABLE CODES --
# ====================


def test_required_field():
    printc("[bold bright_white]TESTING ALL THE FIELDS WITH BAD DATA[/bold bright_white]")
    # https://stackoverflow.com/questions/1278705/when-i-catch-an-exception-how-do-i-get-the-type-file-and-line-number
    try:
        DRIVER.refresh()
        time.sleep(2)
        DRIVER.find_element(By.CLASS_NAME, "nav-button").click()
        time.sleep(1)

        DRIVER.find_element(By.XPATH,
                            "//p[normalize-space()='Proceed Next']"
                            ).click()

        err = DRIVER.find_elements(By.CLASS_NAME, "error-message")
        assert len(err) > 0, "[bold bright_red][ BUG ][/bold bright_red] Error message did not appear"

        printc("[bold green][ SUCCESS ][/bold green]"
               " Required Filed Validation Test Passed")

    except Exception:
        exc_type, _, exc_tb = sys.exc_info()
        if exc_tb is not None:
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            printc("[bold bright_red][ ERROR ][/bold bright_red]",
                   exc_type, fname, exc_tb.tb_lineno)


def test_invalid_inputs():
    try:
        DRIVER.refresh()
        time.sleep(2)

        DRIVER.find_element(By.CLASS_NAME, "nav-button").click()
        time.sleep(1)

        DRIVER.find_element(By.NAME, "firstname").send_keys("John123")
        DRIVER.find_element(By.NAME, "lastname").send_keys("Doe@#")
        DRIVER.find_element(By.NAME, "email").send_keys("invalidemail")
        DRIVER.find_element(By.NAME, "contact").send_keys("abcd1234")
        DRIVER.find_element(By.NAME, "company").send_keys("Null Company")
        dropdown = Select(DRIVER.find_element(By.ID, "enterpriseIndustry"))
        dropdown.select_by_index(2)

        DRIVER.find_element(By.XPATH,
                            "//p[normalize-space()='Proceed Next']"
                            ).click()

        err = DRIVER.find_elements(By.CLASS_NAME, "error-message")
        assert len(err) > 0, "[bold bright_red][ BUG ][/bold bright_red] Invalid inputs were accepted!"

        printc("[bold green][ SUCCESS ][/bold green]"
               " Invalid Input Handling Test Passed")

    except Exception:
        exc_type, _, exc_tb = sys.exc_info()
        if exc_tb is not None:
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            printc("[bold bright_red][ ERROR ][/bold bright_red]",
                   exc_type, fname, exc_tb.tb_lineno)


def test_injection_SQL():
    try:
        DRIVER.refresh()
        time.sleep(2)

        DRIVER.find_element(By.CLASS_NAME, "nav-button").click()
        time.sleep(1)

        payload = "' OR '1'='1'; --"

        DRIVER.find_element(By.NAME, "firstname").send_keys(payload)
        DRIVER.find_element(By.NAME, "lastname").send_keys(payload)
        DRIVER.find_element(By.NAME, "email").send_keys("test.site@corp.com")
        DRIVER.find_element(By.NAME, "contact").send_keys("06987654321")
        DRIVER.find_element(By.NAME, "company").send_keys(payload)
        dropdown = Select(DRIVER.find_element(By.ID, "enterpriseIndustry"))
        dropdown.select_by_index(2)

        DRIVER.find_element(By.XPATH,
                            "//p[normalize-space()='Proceed Next']"
                            ).click()

        assert "error" in DRIVER.page_source.lower(), "[bold bright_red][ BUG ][/bold bright_red] Vulnerability Detected"

        printc("[bold green][ SUCCESS ][/bold green]"
               " SQL Injection Detection Test Passed")

    except Exception:
        exc_type, _, exc_tb = sys.exc_info()
        if exc_tb is not None:
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            printc("[bold bright_red][ ERROR ][/bold bright_red]",
                   exc_type, fname, exc_tb.tb_lineno)


def test_XSS():
    try:
        DRIVER.refresh()
        time.sleep(2)

        DRIVER.find_element(By.CLASS_NAME, "nav-button").click()
        time.sleep(1)

        payload = "<script>alert('Vulnerabile to XSS')</script>"

        DRIVER.find_element(By.NAME, "firstname").send_keys(payload)
        DRIVER.find_element(By.NAME, "lastname").send_keys(payload)
        DRIVER.find_element(By.NAME, "email").send_keys("test.site@corp.com")
        DRIVER.find_element(By.NAME, "contact").send_keys("06987654321")
        DRIVER.find_element(By.NAME, "company").send_keys(payload)
        dropdown = Select(DRIVER.find_element(By.ID, "enterpriseIndustry"))
        dropdown.select_by_index(2)

        DRIVER.find_element(By.XPATH,
                            "//p[normalize-space()='Proceed Next']"
                            ).click()

        assert "error" in DRIVER.page_source, "[bold bright_red][ BUG ][/bold bright_red] XSS Vulnerability Detected"

        printc("[bold green][ SUCCESS ][/bold green]"
               " Cross Site Scripting Test Passed")

    except Exception:
        exc_type, _, exc_tb = sys.exc_info()
        if exc_tb is not None:
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            printc("[bold bright_red][ ERROR ][/bold bright_red]",
                   exc_type, fname, exc_tb.tb_lineno)


def test_navbar():
    try:
        DRIVER.refresh()
        time.sleep(2)

        nav_links = {
            "Foundry": None,
            "Neural AI": "https://www.xenonstack.com/neural-ai/",
            "NexaStack": "https://nexastack.ai/",
            "ElixirData": "https://www.elixirdata.co/",
            "MetaSecure": "https://metasecure.ai/",
            "Akira AI": "https://akira.ai/",
            "XAI": "https://www.xenonstack.ai/"
        }

        retries = 3  # Retry to handle stale elements or loading issues

        # Wait for the navbar to load
        wait_for_navbar()

        for link_text, expected_url in nav_links.items():
            found = False  # Track if the link was found
            for _ in range(retries):
                try:
                    WebDriverWait(DRIVER, 1).until(
                        EC.presence_of_element_located((
                            By.CSS_SELECTOR,
                            "ul.nav-pointers li.nav-li.item"
                        ))
                    )

                    nav_items = DRIVER.find_elements(
                                        By.CSS_SELECTOR,
                                        "ul.nav-pointers li.nav-li.item"
                    )

                    if not nav_items:
                        printc("[bold bright_red][ ERROR ][/bold bright_red]"
                               "Navbar items not found! Retrying.......")
                        time.sleep(2)
                        continue

                    printc("[bold cyan]Available Navbar Items:[/bold cyan]",
                           [el.text for el in nav_items])

                    item = None
                    for nav_item in nav_items:
                        try:
                            p_element = nav_item.find_element(By.TAG_NAME, "p")
                            if link_text in p_element.text:
                                item = nav_item
                                break
                        except Exception:
                            continue

                    if item:
                        found = True
                        DRIVER.execute_script(
                            "arguments[0].scrollIntoView(true);", item
                        )

                        # **Using JavaScript Click Instead of Selenium Click**
                        DRIVER.execute_script("arguments[0].click();", item)
                        time.sleep(2)

                        # **Wait for the navbar to reload before proceeding**
                        WebDriverWait(DRIVER, 1).until(
                            EC.presence_of_element_located((
                                By.CSS_SELECTOR,
                                "ul.nav-pointers li.nav-li.item"
                            ))
                        )

                        # Verify if scrolling worked
                        if expected_url and "xenonstack" in expected_url:
                            assert expected_url in DRIVER.current_url, f"[bold bright_red][ BUG ][/bold bright_red] Navigation failed for {link_text}"
                        else:
                            printc(
                                "[bold bright_yellow][ WARNING ]",
                                "[/bold bright_yellow]", link_text,
                                " is an external site. Cannot validate.")

                        DRIVER.back()
                        break

                    else:
                        printc("[bold bright_red][ BUG ][/bold bright_red]",
                               "Navigation for ", link_text,
                               " does not work. The Link does not work")
                        break

                except TimeoutException:
                    printc("[bold bright_red][ ERROR ][/bold bright_red]"
                           "Timeout waiting for ",
                           {link_text}, " to be clickable!")
                    break

            if not found:
                printc("[bold bright_red][ BUG ][/bold bright_red]",
                       "Navigation for ", {link_text},
                       "failed. The Link does not work")

        printc("[bold green][ SUCCESS ][/bold green]",
               "Navigation Test Completed")

    except Exception as e:
        exc_type, _, exc_tb = sys.exc_info()
        if exc_tb is not None:
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            printc("[bold bright_red][ ERROR ][/bold bright_red]", exc_type,
                   fname, exc_tb.tb_lineno, str(e))


if __name__ == "__main__":
    # test_required_field()
    # test_invalid_inputs()
    # test_injection_SQL()
    # test_XSS()
    test_navbar()
    DRIVER.quit()
