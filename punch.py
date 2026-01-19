from playwright.sync_api import sync_playwright
from datetime import datetime
import os

LMS_URL = os.getenv("LMS_URL")
USERNAME = os.getenv("LMS_USER")
PASSWORD = os.getenv("LMS_PASS")

now = datetime.now().hour

ACTION = "IN" if now < 12 else "OUT"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(LMS_URL)

    page.fill("input[type='text']", USERNAME)
    page.fill("input[type='password']", PASSWORD)
    page.click("button")

    page.wait_for_timeout(5000)

    if ACTION == "IN":
        page.click("text=Punch In")
    else:
        page.click("text=Punch Out")

    browser.close()
