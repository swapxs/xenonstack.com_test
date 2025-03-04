# /functional/helpers/form_handler.py
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

logger = logging.getLogger(__name__)

# Function for injecting malicious code into the input fields of the form
# This may be an SQL injection or an XSS.
def injkt(driver, payload):
    fields = ["firstname", "lastname", "company"]

    logger.warning(f"Injecting payload '{payload}' into multiple fields.")
    
    for field in fields:
        driver.find_element(By.NAME, field).send_keys(payload)

    driver.find_element(By.NAME, "email").send_keys("test.site@corp.com")
    driver.find_element(By.NAME, "contact").send_keys("06987654321")

    Select(driver.find_element(By.ID, "enterpriseIndustry")).select_by_index(2)

# Function that fills up the form with the provided data
def fill_xenon_form(driver, fname, lname, email, num, cmpny):
    logger.info("Filling the form with provided user details.")

    fields = {
        "firstname": fname,
        "lastname": lname,
        "email": email,
        "contact": num,
        "company": cmpny
    }

    for field_name, value in fields.items():
        logger.info(f"Entering {field_name.capitalize()}: {value}")
        driver.find_element(By.NAME, field_name).send_keys(value)

    Select(driver.find_element(By.ID, "enterpriseIndustry")).select_by_index(2)
