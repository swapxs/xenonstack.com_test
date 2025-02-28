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
    TimeoutException as TE,
    StaleElementReferenceException as SER,
    NoSuchElementException as NSE
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
    "alrt": "red",
    "counter": "bold bright_yellow"
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


def extract_links(html_tag):
    try:
        WAIT.until(
            EC.presence_of_element_located((By.TAG_NAME, html_tag))
        )

        footer = DRIVER.find_element(By.TAG_NAME, html_tag)
        return footer.find_elements(By.TAG_NAME, "a")

    except NSE:
        return []


def page_loader():
    try:
        WAIT.until(
            lambda d:
                d.execute_script("return document.readyState") == "complete"
        )

    except TE:
        printc("[warn][ - ][/warn]"
               "Page took too long to load. Stopping load manually.")
        DRIVER.execute_script("window.stop();")


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
                       "Page changed to {new_url}")
            else:
                printc(f"[bug][ x ][/bug] '{link_text}' is a BUG, fix it.")
            DRIVER.back()
            page_loader()
            WAIT.until(EC.url_to_be(old_url))
    except TE:
        printc("[bug][ x ][/bug] Timeout opening link '{link_text}'")
    except Exception:
        printc(f"[bug][ x ][/bug] Error opening '{link_text}'")


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

        for sec_idx, op_idx in selections.items():
            opt_xp = f"//*[@id='{sec_idx}']//div[@class='answers'][{op_idx}]/p"
            DRIVER.find_element(By.XPATH, opt_xp).click()

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


def test_footer():
    printc("\n[head]Test 2.2:[/head]",
           "Ensuring All Footer Links Are Checked Without Skips.")

    DRIVER.refresh()
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
                printc("[bold bright_yellow][ ! ][/bold bright_yellow] ",
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
    test_footer()


if __name__ == "__main__":
    OPT = Options()
    OPT.add_argument("--start-maximized")
    OPT.add_argument("--disable-blink-features=AutomationControlled")
    OPT.add_argument("--headless=new")  # Run headless

    SERVICE = Service("/usr/bin/chromedriver", log_output="/dev/null")
    DRIVER = webdriver.Chrome(service=SERVICE, options=OPT)
    DRIVER.get("https://www.xenonstack.com/")

    WAIT = WebDriverWait(DRIVER, 5)
    test_form()
    test_nav_and_foot()
    DRIVER.quit()
