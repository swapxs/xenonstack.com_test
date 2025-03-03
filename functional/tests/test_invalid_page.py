from utils.rich_config import printc
from utils.selenium_config import DRIVER
from helpers.page_loader import page_loader


def test_invalid_page():
    printc("\n[head]Test 4.2: [/head] Checking 404 Error Handling")

    DRIVER.get("https://xenonstack.com/this-page-does-not-exist")
    page_loader()

    title = DRIVER.title.lower()
    src = DRIVER.page_source.lower()

    if "404" in title or "not found" in src:
        printc("[success][ + ][/success] 404 page correctly displayed.")
    else:
        printc("[bug][ x ][/bug] 404 page is missing or incorrect!")
