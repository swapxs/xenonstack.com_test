# conftest.py

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture
def driver():
    opt = Options()
    opt.add_argument("--start-maximized")
    opt.add_argument("--disable-blink-features=AutomationControlled")
    opt.add_argument("--headless=new")  # Run headless

    # Replace with your actual path to chromedriver
    service = Service("/usr/bin/chromedriver", log_output="/dev/null")

    driver = webdriver.Chrome(service=service, options=opt)
    driver.set_page_load_timeout(15)
    yield driver
    driver.quit()


@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, 10)
