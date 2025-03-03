from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

OPT = Options()
OPT.add_argument("--start-maximized")
OPT.add_argument("--disable-blink-features=AutomationControlled")
OPT.add_argument("--headless=new")  # Run headless

SERVICE = Service("/usr/bin/chromedriver", log_output="/dev/null")
DRIVER = webdriver.Chrome(service=SERVICE, options=OPT)
DRIVER.get("https://www.xenonstack.com/")

WAIT = WebDriverWait(DRIVER, 5)
