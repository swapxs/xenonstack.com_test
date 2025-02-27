import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
# https://github.com/Textualize/rich?tab=readme-ov-file
from rich.console import Console
from rich.theme import Theme

custom_theme = Theme({
    "success": "bold bright_green",
    "head": "bold bright_white",
    "info": "dim cyan",
    "warn": "bold magenta",
    "bug": "bold bright_red",
    "alrt": "dim red"
})


printc = Console(theme=custom_theme).print

OPT = Options()
OPT.add_argument("--start-maximized")
OPT.add_argument("--disable-blink-features=AutomationControlled")
OPT.add_argument("--headless=new")  # Run headless

SERVICE = Service("/usr/bin/chromedriver", log_output="/dev/null")
DRIVER = webdriver.Chrome(service=SERVICE, options=OPT)
DRIVER.get("https://www.xenonstack.com/")

# ======================
# -- HELPER FUNCTIONS --
# ======================


def get_nav_items():
    WebDriverWait(DRIVER, 5).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "ul.nav-pointers")
        )
    )

    return DRIVER.find_elements(
        By.CSS_SELECTOR, "ul.nav-pointers li.nav-li.item"
    )


def injkt(payload):
    printc("\t[warn][ - ][/warn] Sending ", payload,
           " as Firstname")
    DRIVER.find_element(By.NAME, "firstname").send_keys(payload)

    printc("\t[warn][ - ][/warn] Sending ", payload,
           " as Lastname")
    DRIVER.find_element(By.NAME, "lastname").send_keys(payload)

    DRIVER.find_element(By.NAME, "email").send_keys("test.site@corp.com")
    DRIVER.find_element(By.NAME, "contact").send_keys("06987654321")

    printc("\t[warn][ - ][/warn] Sending ", payload,
           " as Company Name")
    DRIVER.find_element(By.NAME, "company").send_keys(payload)

    dropdown = Select(DRIVER.find_element(By.ID, "enterpriseIndustry"))
    dropdown.select_by_index(2)


# ====================
# -- TEST FUNCTIONS --
# ====================


def test_required_field():
    printc("\n[head]Test 1: [/head]"
           " Testing For Required Fileds.")

    # https://stackoverflow.com/questions/1278705/when-i-catch-an-exception-how-do-i-get-the-type-file-and-line-number
    try:
        DRIVER.refresh()
        time.sleep(2)
        printc("[bold yellow][ * ][/bold yellow] Get Started Button Clicked")
        DRIVER.find_element(By.CLASS_NAME, "nav-button").click()
        time.sleep(1)

        printc("[bold yellow][ * ][/bold yellow] Proceed Next Button Clicked")
        DRIVER.find_element(By.XPATH,
                            "//p[normalize-space()='Proceed Next']"
                            ).click()

        err = DRIVER.find_elements(By.CLASS_NAME, "error-message")

        assert len(err) > 0, \
            "[bug][ x ][/bug]" \
            " Error message did not appear." \
            " Test [bug]Failed[/bug]"

        printc("[success][ + ][/success]"
               " Required Filed Validation Test",
               "[success]Passed[/success]."
               " It does not let us go through without entering data.")

    except Exception:
        exc_type, _, exc_tb = sys.exc_info()
        if exc_tb is not None:
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            printc("[bug][ x ][/bug]",
                   exc_type, fname, exc_tb.tb_lineno)


def test_invalid_inputs():
    printc("\n[head]Test 2: [/head]"
           " Testing For Invalid Inputs.")

    try:
        DRIVER.refresh()
        time.sleep(2)

        printc("[bold yellow][ * ][/bold yellow] Get Started Button Clicked")
        DRIVER.find_element(By.CLASS_NAME, "nav-button").click()
        time.sleep(1)

        fname = "John123"
        lname = "Doe@#"
        email = "invalidemail"
        num = "abcd1234"
        cmpny = "Null Company"

        printc("[bold yellow][ * ][/bold yellow] Filling the Form")

        printc("\t[warn][ - ][/warn] Entered FirstName: ",
               fname)
        DRIVER.find_element(By.NAME, "firstname").send_keys(fname)

        printc("\t[warn][ - ][/warn] Entered Lastname: ",
               lname)
        DRIVER.find_element(By.NAME, "lastname").send_keys(lname)

        printc("\t[warn][ - ][/warn] Entered Email: ", email)
        DRIVER.find_element(By.NAME, "email").send_keys(email)

        printc("\t[warn][ - ][/warn] Entered Contact: ", num)
        DRIVER.find_element(By.NAME, "contact").send_keys(num)

        printc("\t[warn][ - ][/warn] Entered Company: ", cmpny)
        DRIVER.find_element(By.NAME, "company").send_keys(cmpny)
        dropdown = Select(DRIVER.find_element(By.ID, "enterpriseIndustry"))
        dropdown.select_by_index(2)

        printc("[bold yellow][ * ][/bold yellow] Proceed Next Button Clicked")
        DRIVER.find_element(By.XPATH,
                            "//p[normalize-space()='Proceed Next']"
                            ).click()

        err = DRIVER.find_elements(By.CLASS_NAME, "error-message")
        assert len(err) > 0, \
            "[bug][ x ][/bug]" \
            " Invalid inputs were accepted!"

        printc("[success][ + ][/success]"
               " Input Validation Testing ",
               "[success]Passed[/success]."
               " Does not let us go through without providing proper inputs.")

    except Exception:
        exc_type, _, exc_tb = sys.exc_info()
        if exc_tb is not None:
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            printc("[bug][ x ][/bug]",
                   exc_type, fname, exc_tb.tb_lineno)


def test_injection_SQL():
    printc("\n[head]Test 3: [/head]"
           " Testing For SQL Injection.")
    try:
        DRIVER.refresh()
        time.sleep(2)

        printc("[bold yellow][ * ][/bold yellow] Get Started Button Clicked")
        DRIVER.find_element(By.CLASS_NAME, "nav-button").click()
        time.sleep(1)

        injkt("' OR '1'='1'; --")

        printc("[bold yellow][ * ][/bold yellow] Proceed Next Button Clicked")
        DRIVER.find_element(By.XPATH,
                            "//p[normalize-space()='Proceed Next']"
                            ).click()

        assert "error" in DRIVER.page_source.lower(), \
            "[bug][ x ][/bug] Vulnerability Detected"

        printc("[success][ + ][/success]"
               " SQL Injection Detection Test Passed")

    except Exception:
        exc_type, _, exc_tb = sys.exc_info()
        if exc_tb is not None:
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            printc("[bug][ x ][/bug]",
                   exc_type, fname, exc_tb.tb_lineno)


def test_XSS():
    printc("\n[head]Test 4: [/head]"
           " Testing For Script Injection or Cross Site Scripting (XSS)")
    try:
        DRIVER.refresh()
        time.sleep(2)

        printc("[bold yellow][ * ][/bold yellow] Get Started Button Clicked")
        DRIVER.find_element(By.CLASS_NAME, "nav-button").click()
        time.sleep(1)

        injkt("<script>alert('Vulnerabile to XSS')</script>")

        printc("[bold yellow][ * ][/bold yellow] Proceed Next Button Clicked")
        DRIVER.find_element(By.XPATH,
                            "//p[normalize-space()='Proceed Next']"
                            ).click()

        assert "error" in DRIVER.page_source, \
            "[bug][ x ][/bug]" \
            " XSS Vulnerability Detected."

        printc("[success][ + ][/success]"
               " Cross Site Scripting Test Passed")

    except Exception:
        exc_type, _, exc_tb = sys.exc_info()
        if exc_tb is not None:
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            printc("[bug][ x ][/bug]",
                   exc_type, fname, exc_tb.tb_lineno)


def test_navbar():
    printc("\n[head]Test 5: [/head]"
           " Testing The Navigation Bar In The Website")
    try:
        DRIVER.refresh()
        time.sleep(2)

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

                except NoSuchElementException:
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

            except StaleElementReferenceException:
                printc("[bug][ x ][/bug]"
                       " [alrt]BUG:[/alrt] Stale element error for ",
                       link_text)

            except TimeoutException:
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


if __name__ == "__main__":
    test_required_field()
    test_invalid_inputs()
    test_injection_SQL()
    test_XSS()
    test_navbar()
    DRIVER.quit()
