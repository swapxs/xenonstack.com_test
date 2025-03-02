from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from utils.rich_config import printc
from utils.selenium_config import (
    DRIVER
)


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

