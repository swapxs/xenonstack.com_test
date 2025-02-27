import os
import sys
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    NoSuchElementException
)
# https://github.com/Textualize/rich?tab=readme-ov-file
from rich.console import Console
from rich.theme import Theme

custom_theme = Theme({
    "success": "bold bright_green",
    "head": "bold bright_white",
    "info": "dim cyan",
    "warn": "bold magenta",
    "bug": "bold bright_red",
    "alrt": "red"
})


printc = Console(theme=custom_theme).print

# ======================
# -- HELPER FUNCTIONS --
# ======================


# Function for getting all the items in the navigation bar
def get_nav_items():
    WAIT.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "ul.nav-pointers")
        )
    )

    return DRIVER.find_elements(
        By.CSS_SELECTOR, "ul.nav-pointers li.nav-li.item"
    )


def get_footer_items():
    try:
        footer = DRIVER.find_element(By.TAG_NAME, "footer")
        return footer.find_elements(By.TAG_NAME, "a")
    except NoSuchElementException:
        return []


# Function for injecting malicious code into the input files for the form
# This may be as simple as an SQL injection or a XSS.
def injkt(payload):
    fields = ["firstname", "lastname", "company"]

    printc("\t[warn][ - ][/warn] Sending ", payload, " to multiple fields.")
    for field in fields:
        DRIVER.find_element(By.NAME, field).send_keys(payload)
        pass

    DRIVER.find_element(By.NAME, "email").send_keys("test.site@corp.com")
    DRIVER.find_element(By.NAME, "contact").send_keys("06987654321")

    Select(DRIVER.find_element(By.ID, "enterpriseIndustry")).select_by_index(2)


# Function that fills up the form with the data passed through the parameters
def fill_xenon_form(fname, lname, email, num, cmpny):
    printc("[bold yellow][ * ][/bold yellow] Filling the Form")

    fields = {
        "firstname": fname,
        "lastname": lname,
        "email": email,
        "contact": num,
        "company": cmpny
    }

    for field_name, value in fields.items():
        printc("\t[warn][ - ][/warn] Entered",
               field_name.capitalize(),
               ": ",
               value)

        DRIVER.find_element(By.NAME, field_name).send_keys(value)

    Select(DRIVER.find_element(By.ID, "enterpriseIndustry")).select_by_index(2)

# ====================
# -- TEST FUNCTIONS --
# ====================


# This function tests if the fileds in the form are "required" by nature and
# checks if we can proceed and see to content of the next page without filling
# up the form.
def test_required_field():
    printc("[head]Test 1.1: [/head]"
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
    printc("\n[head]Test 1.2: [/head]"
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

        fill_xenon_form(fname, lname, email, num, cmpny)

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


def test_valid_inputs():
    printc("\n[head]Test 1.3: [/head]"
           " Testing For Invalid Inputs.")

    try:
        DRIVER.refresh()
        time.sleep(2)

        printc("[bold yellow][ * ][/bold yellow] Get Started Button Clicked")
        DRIVER.find_element(By.CLASS_NAME, "nav-button").click()
        time.sleep(1)

        fname = "Jack"
        lname = "Doe"
        email = "nucmpny@gmail.com"
        num = "05987654312"
        cmpny = "Testify"

        fill_xenon_form(fname, lname, email, num, cmpny)

        printc("[bold yellow][ * ][/bold yellow] Proceed Next Button Clicked")
        DRIVER.find_element(By.XPATH,
                            "//p[normalize-space()='Proceed Next']"
                            ).click()

        selections = {
                "agenticaiPlatform": 1,
                "companySegment": 2,
                "primaryFocus": 2,
                "aiUsecase": 1,
                "primaryChallenge": 5,
                "companyInfra": 1,
                "dataPlatform": 1,
                "aiTransformation": 1,
                "solution": 2
            }

        for section_id, option_index in selections.items():
            option_xpath = f"//*[@id='{section_id}']//div[@class='answers'][{option_index}]/p"
            DRIVER.find_element(By.XPATH, option_xpath).click()

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
    printc("\n[head]Test 1.4: [/head]"
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


def test_injection_XSS():
    printc("\n[head]Test 1.5: [/head]"
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
    printc("\n[head]Test 2.1: [/head]"
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


def test_footer():
    printc("\n[head]Test 2.2 (Optimized): [/head]"
           " Testing The Footer Links with Reduced Load Time")

    DRIVER.set_page_load_timeout(5)  # General timeout for the whole test

    DRIVER.refresh()
    time.sleep(1)  # Ensure page is loaded before interacting

    # Re-find footer links to avoid stale elements
    footer_links = get_footer_items()
    if not footer_links:
        printc("[bug][ x ][/bug] FOOTER TEST FAILED - No links found in the footer!")
        return

    printc("[info]Available Footer Links: [/info]",
           [link.text.strip() for link in footer_links if link.text.strip()])

    for idx, link in enumerate(footer_links, start=1):
        try:
            # Re-find elements to prevent stale references
            footer_links = get_footer_items()
            link = footer_links[idx - 1]

            link_text = link.text.strip()
            href = link.get_attribute("href")
            target = link.get_attribute("target")

            # If the link has no visible text, try using <img alt="...">
            if not link_text:
                try:
                    img = link.find_element(By.TAG_NAME, "img")
                    alt_text = img.get_attribute("alt")
                    if alt_text:
                        link_text = alt_text.strip()
                except NoSuchElementException:
                    pass
                if not link_text:
                    link_text = "(no text)"

            # Skip links with no href
            if not href:
                printc(f"[bug][ x ][/bug] Skipping '{link_text}' - No href attribute.")
                continue

            printc(f"[bold bright_yellow][ ! ][/bold bright_yellow] "
                   f"[{idx}/{len(footer_links)}] Checking Footer Link: {href} -> {link_text}")

            # If external, perform a HEAD request first
            if "xenonstack.com" not in href.lower():
                try:
                    resp = requests.get(href, timeout=2, stream=True)  # GET to avoid 403
                    if resp.status_code < 400:
                        printc("[success][ + ][/success]"
                               f" External link '{link_text}' is valid. [HTTP {resp.status_code}]")
                    else:
                        printc("[bug][ x ][/bug]"
                               f" '{link_text}' returned HTTP {resp.status_code}")
                except requests.RequestException as e:
                    printc("[bug][ x ][/bug]"
                           f" Failed request for '{link_text}': {str(e)}")

            else:
                # Internal Link => Click and validate page load
                old_url = DRIVER.current_url
                try:
                    if target == "_blank":
                        DRIVER.execute_script("window.open(arguments[0]);", href)
                        time.sleep(0.3)
                        all_handles = DRIVER.window_handles
                        if len(all_handles) > 1:
                            DRIVER.switch_to.window(all_handles[-1])
                            new_url = DRIVER.current_url
                            if new_url != old_url and new_url != "data:,":
                                printc("[success][ + ][/success]"
                                       f" '{link_text}' opened in new tab - OK")
                            else:
                                printc("[bug][ x ][/bug]"
                                       f" '{link_text}' new tab did not navigate.")
                            DRIVER.close()
                            DRIVER.switch_to.window(all_handles[0])
                        else:
                            printc("[bug][ x ][/bug]"
                                   f" No new tab detected for '{link_text}'")
                    else:
                        DRIVER.execute_script("arguments[0].click();", link)
                        time.sleep(0.3)
                        new_url = DRIVER.current_url
                        if new_url != old_url and new_url != "data:,":
                            printc("[success][ + ][/success]"
                                   f" '{link_text}' link works - Page changed to {new_url}")
                        else:
                            printc("[bug][ x ][/bug]"
                                   f" '{link_text}' did nothing or redirected to data:, BUG?")
                        DRIVER.back()
                        time.sleep(0.2)

                except TimeoutException:
                    printc("[bug][ x ][/bug]"
                           f" Timeout opening link '{link_text}'")
                except Exception as e:
                    printc("[bug][ x ][/bug]"
                           f" Error opening '{link_text}': {str(e)}")

        except StaleElementReferenceException:
            printc("[bug][ x ][/bug] Stale element error. Re-fetching and retrying...")

    printc("[success][ + ][/success]"
           " Optimized Footer Test Completed Successfully")


# CONSOLIDATED TESTS
#

def test_form():
    printc("\n[head]Test 1: [/head]"
           " Get Started Form Validation Tests.")

    test_required_field()
    test_invalid_inputs()
    test_valid_inputs()
    test_injection_SQL()
    test_injection_XSS()


def test_nav_and_foot():
    printc("\n[head]Test 2: [/head]"
           " Navigation Bar and Footer Tests.")

    test_navbar()


if __name__ == "__main__":
    OPT = Options()
    OPT.add_argument("--start-maximized")
    OPT.add_argument("--disable-blink-features=AutomationControlled")
    OPT.add_argument("--headless=new")  # Run headless

    SERVICE = Service("/usr/bin/chromedriver", log_output="/dev/null")
    DRIVER = webdriver.Chrome(service=SERVICE, options=OPT)
    DRIVER.get("https://www.xenonstack.com/")

    WAIT = WebDriverWait(DRIVER, 5)
    # test_form()
    # test_nav_and_foot()
    test_footer()
    DRIVER.quit()
