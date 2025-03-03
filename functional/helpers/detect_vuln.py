import logging
from selenium.webdriver.common.alert import Alert

# Configure logger
logger = logging.getLogger(__name__)

def detect_vuln(driver):
    """
    Detects if an XSS alert appears on the webpage.
    If an alert is found, logs the message and returns True.
    Otherwise, returns False.
    """
    try:
        txt = Alert(driver).text
        Alert(driver).dismiss()
        logger.warning(f"XSS Alert Detected! Message: {txt}")
        return True

    except Exception:
        logger.info("No XSS Alert detected.")
        return False
