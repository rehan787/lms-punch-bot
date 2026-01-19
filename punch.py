from playwright.sync_api import sync_playwright
import os
import time

# LMS URL & credentials from environment variables
LMS_URL = os.getenv("LMS_URL")
USERNAME = os.getenv("LMS_USER")
PASSWORD = os.getenv("LMS_PASS")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # 1️⃣ Open LMS login page
    page.goto(LMS_URL, wait_until="load", timeout=60000)  # 60 sec max

    # 2️⃣ Wait for USERNAME input field
    page.wait_for_selector("#ctl03_txtuser", state="visible", timeout=60000)
    page.fill("#ctl03_txtuser", USERNAME)

    # 3️⃣ Wait for PASSWORD input field
    page.wait_for_selector("#ctl03_txtpassword", state="visible", timeout=60000)
    page.fill("#ctl03_txtpassword", PASSWORD)

    # 4️⃣ Wait for LOGIN button and click
    page.wait_for_selector("#ctl03_btnLogin", state="visible", timeout=60000)
    page.click("#ctl03_btnLogin")

    # 5️⃣ Wait for dashboard to fully load
    page.wait_for_load_state("networkidle", timeout=60000)
    time.sleep(2)  # small buffer for JS

    # 6️⃣ Wait for PUNCH button
    page.wait_for_selector("button.btn.btn-warning.btn-large.bg-color", state="visible", timeout=60000)
    time.sleep(1)  # small buffer
    page.click("button.btn.btn-warning.btn-large.bg-color")

    # 7️⃣ Close browser
    browser.close()
