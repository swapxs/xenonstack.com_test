from utils.rich_config import printc
from utils.selenium_config import (
    WAIT,
    DRIVER
)
from selenium.common.exceptions import TimeoutException as TE

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

