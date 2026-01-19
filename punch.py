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

    # 2️⃣ Fill username using XPath + force-fill
    username_xpath = "/html/body/form/div[3]/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/div/table/tbody/tr[2]/td/input[1]"
    page.wait_for_selector(f"xpath={username_xpath}", timeout=60000)
    time.sleep(1)
    page.evaluate(f"""
        document.evaluate("{username_xpath}", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null)
        .singleNodeValue.value = "{USERNAME}";
    """)

    # 3️⃣ Fill password using XPath + force-fill
    password_xpath = "/html/body/form/div[3]/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/div/table/tbody/tr[3]/td/input[1]"
    page.wait_for_selector(f"xpath={password_xpath}", timeout=60000)
    time.sleep(1)
    page.evaluate(f"""
        document.evaluate("{password_xpath}", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null)
        .singleNodeValue.value = "{PASSWORD}";
    """)

    # 4️⃣ Click login button (ID)
    page.wait_for_selector("#ctl03_btnLogin", timeout=60000)
    time.sleep(1)
    page.click("#ctl03_btnLogin")

    # 5️⃣ Wait for dashboard to load fully
    page.wait_for_load_state("networkidle", timeout=60000)
    time.sleep(3)  # small buffer for JS

    # 6️⃣ Punch button (class/text)
    page.wait_for_selector("button.btn.btn-warning.btn-large.bg-color", timeout=60000)
    time.sleep(1)
    page.click("button.btn.btn-warning.btn-large.bg-color")

    # 7️⃣ Close browser
    browser.close()
    print("Punch action completed successfully!")
