from utils.rich_config import printc
from tests.test_navbar import test_navbar
from tests.test_footer import test_footer
from tests.test_load_speed import test_load_speed
from tests.test_invalid_page import test_invalid_page
from tests.test_form import (
    test_required_field,
    test_invalid_inputs,
    test_valid_inputs,
)

from tests.test_security import (
    test_injection_SQL,
    test_injection_XSS
)


# ==================================================================================
# SCENARIO_1: A User want to get started with xenonstack
# ==================================================================================

def test_form():
    printc("\n[head]Test 1: [/head]"
           " Get Started Form Validation Tests.")

    test_required_field()
    test_invalid_inputs()
    test_valid_inputs()


# ==================================================================================
# SCENARIO_2: A Malicious User wants to send some bad sql and javascript
#             commands to gain priviledged user access to the system. We need
#             to verify that the form does not allow us to do that.
# ==================================================================================


def test_security():
    printc("\n[head]Test 2: [/head]"
           " Testing the Security of the website's Form.")
    test_injection_SQL()
    test_injection_XSS()


# ==================================================================================
# SCENARIO_3: A User wants to visit daughter sites from either the NAVIGATION
#             BAR or the FOOTER LINKS
# ==================================================================================


def test_nav_and_foot():
    printc("\n[head]Test 3: [/head]"
           " Navigation Bar and Footer Tests.")

    test_navbar()
    test_footer()


# ==================================================================================
# SCENARIO_4: Check website performace and ability to hold its gound under
#             stress.
# ==================================================================================


def test_performance():
    printc("\n[head]Test 4: [/head]"
           " Site Performance Tests.")
    test_load_speed()
    test_invalid_page()


if __name__ == "__main__":
    # ------ TESTS ------
    test_form()
    test_nav_and_foot()
    test_performance()
    # ------ TESTS ------
