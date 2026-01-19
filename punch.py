from playwright.sync_api import sync_playwright
import os
import time

# -----------------------------
# LMS URL & credentials
# -----------------------------
LMS_URL = os.getenv("LMS_URL")
USERNAME = os.getenv("LMS_USER")
PASSWORD = os.getenv("LMS_PASS")

# -----------------------------
# Main automation
# -----------------------------
with sync_playwright() as p:
    # Launch headless browser
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # 1️⃣ Open LMS login page
    page.goto(LMS_URL, wait_until="load", timeout=60000)  # max 1 minute

    # 2️⃣ Wait for username input to exist, then force-fill
    page.wait_for_selector("#ctl03_txtuser", timeout=60000)
    time.sleep(1)  # buffer for JS / WaterMark
    page.evaluate(f"document.querySelector('#ctl03_txtuser').value = '{USERNAME}';")

    # 3️⃣ Wait for password input to exist, then force-fill
    page.wait_for_selector("#ctl03_txtpassword", timeout=60000)
    time.sleep(1)
    page.evaluate(f"document.querySelector('#ctl03_txtpassword').value = '{PASSWORD}';")

    # 4️⃣ Wait for login button and click
    page.wait_for_selector("#ctl03_btnLogin", timeout=60000)
    time.sleep(1)
    page.click("#ctl03_btnLogin")

    # 5️⃣ Wait for dashboard to load fully
    page.wait_for_load_state("networkidle", timeout=60000)
    time.sleep(3)  # small buffer for JS rendering

    # 6️⃣ Wait for punch button to appear and click
    page.wait_for_selector("button.btn.btn-warning.btn-large.bg-color", timeout=60000)
    time.sleep(1)
    page.click("button.btn.btn-warning.btn-large.bg-color")

    # 7️⃣ Close browser
    browser.close()

    # ✅ Finished
    print("Punch action completed successfully!")
