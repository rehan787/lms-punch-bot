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
# XPaths
# -----------------------------
USERNAME_XPATH = "/html/body/form/div[3]/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/div/table/tbody/tr[2]/td/input[1]"
PASSWORD_XPATH = "/html/body/form/div[3]/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/div/div/div/table/tbody/tr[3]/td/input[1]"
PUNCH_BUTTON_SELECTOR = "button.btn.btn-warning.btn-large.bg-color"

# -----------------------------
# Main automation
# -----------------------------
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # 1️⃣ Open LMS login page
    page.goto(LMS_URL, wait_until="load", timeout=60000)  # max 1 min

    # -----------------------------
    # 2️⃣ Poll & fill username
    # -----------------------------
    for _ in range(60):  # max 60 seconds
        exists = page.evaluate(f"""
            document.evaluate("{USERNAME_XPATH}", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null)
            .singleNodeValue != null
        """)
        if exists:
            page.evaluate(f"""
                document.evaluate("{USERNAME_XPATH}", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null)
                .singleNodeValue.value = "{USERNAME}";
            """)
            break
        time.sleep(1)
    else:
        raise Exception("Username input not found after 60 seconds")

    # -----------------------------
    # 3️⃣ Poll & fill password
    # -----------------------------
    for _ in range(60):  # max 60 seconds
        exists = page.evaluate(f"""
            document.evaluate("{PASSWORD_XPATH}", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null)
            .singleNodeValue != null
        """)
        if exists:
            page.evaluate(f"""
                document.evaluate("{PASSWORD_XPATH}", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null)
                .singleNodeValue.value = "{PASSWORD}";
            """)
            break
        time.sleep(1)
    else:
        raise Exception("Password input not found after 60 seconds")

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
    time.sleep(3)

    # -----------------------------
    # 6️⃣ Click punch button
    # -----------------------------
    for _ in range(60):  # max 60 seconds
        exists = page.evaluate(f"""
            document.querySelector("{PUNCH_BUTTON_SELECTOR}") != null
        """)
        if exists:
            page.click(PUNCH_BUTTON_SELECTOR)
            break
        time.sleep(1)
    else:
        raise Exception("Punch button not found after 60 seconds")

    # -----------------------------
    # 7️⃣ Close browser
    # -----------------------------
    browser.close()
    print("Punch action completed successfully!")
