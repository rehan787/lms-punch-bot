from playwright.sync_api import sync_playwright
import os
import time

LMS_URL = os.getenv("LMS_URL")
USERNAME = os.getenv("LMS_USER")
PASSWORD = os.getenv("LMS_PASS")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(LMS_URL, wait_until="load", timeout=60000)

    # 1️⃣ Get the login iframe
    # If multiple iframes, use frame name/id instead of first()
    frame = page.frame_locator("iframe").first

    # 2️⃣ Fill username
    frame.locator("#ctl03_txtuser").fill(USERNAME)

    # 3️⃣ Fill password
    frame.locator("#ctl03_txtpassword").fill(PASSWORD)

    # 4️⃣ Click login
    frame.locator("#ctl03_btnLogin").click()

    # 5️⃣ Wait for dashboard to load fully
    page.wait_for_load_state("networkidle", timeout=60000)
    time.sleep(3)

    # 6️⃣ Punch button on main page
    page.wait_for_selector("button.btn.btn-warning.btn-large.bg-color", timeout=60000)
    time.sleep(1)
    page.click("button.btn.btn-warning.btn-large.bg-color")

    browser.close()
    print("Punch action completed successfully!")
