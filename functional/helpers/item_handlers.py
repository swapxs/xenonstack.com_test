# /helpers/item_handlers.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


# Function for getting all the items in the navigation bar
def get_nav_items(driver, wait):
    wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "ul.nav-pointers")
        )
    )

    return driver.find_elements(
        By.CSS_SELECTOR, "ul.nav-pointers li.nav-li.item"
    )
