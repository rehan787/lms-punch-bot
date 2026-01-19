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
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # 1️⃣ Open LMS login page
    page.goto(LMS_URL, wait_until="load", timeout=60000)  # max 1 min

    # -----------------------------
    # 2️⃣ Fill username (force via JS)
    # -----------------------------
    username_xpath = "/html/body/form/div[3]/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/div/table/tbody/tr[2]/td/input[1]"
    page.wait_for_selector(f"xpath={username_xpath}", state="attached", timeout=60000)
    time.sleep(1)
    page.evaluate(f"""
        document.evaluate("{username_xpath}", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null)
        .singleNodeValue.value = "{USERNAME}";
    """)

    # -----------------------------
    # 3️⃣ Fill password (force via JS)
    # -----------------------------
    password_xpath = "/html/body/form/div[3]/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/div/table/tbody/tr[3]/td/input[1]"
    page.wait_for_selector(f"xpath={password_xpath}", state="attached", timeout=60000)
    time.sleep(1)
    page.evaluate(f"""
        document.evaluate("{password_xpath}", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null)
        .singleNodeValue.value = "{PASSWORD}";
    """)

    # -----------------------------
    # 4️⃣ Click login button
    # -----------------------------
    page.wait_for_selector("#ctl03_btnLogin", state="attached", timeout=60000)
    time.sleep(1)
    page.click("#ctl03_btnLogin")

    # -----------------------------
    # 5️⃣ Wait for dashboard to load fully
    # -----------------------------
    page.wait_for_load_state("networkidle", timeout=60000)
    time.sleep(3)  # small buffer for JS

    # -----------------------------
    # 6️⃣ Click punch button
    # -----------------------------
    punch_selector = "button.btn.btn-warning.btn-large.bg-color"
    page.wait_for_selector(punch_selector, timeout=60000)
    time.sleep(1)
    page.click(punch_selector)

    # -----------------------------
    # 7️⃣ Close browser
    # -----------------------------
    browser.close()
    print("Punch action completed successfully!")
