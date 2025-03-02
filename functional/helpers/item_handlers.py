from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utils.selenium_config import (
    WAIT,
    DRIVER
)

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


