from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

EMAIL = "kumarsharma2580@gmail.com"
LOGIN_URL = "https://www.canva.com/en_in/login/"

options = Options()
options.add_argument("--headless")  # Render ke liye
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 30)

driver.get(LOGIN_URL)

# ===============================
# 1️⃣ Click "Continue with phone number"
# ===============================
continue_btn = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "//button[.//p[contains(text(),'Continue')]]"
    ))
)
continue_btn.click()
print("Clicked continue button")

# ===============================
# 2️⃣ Enter Email
# ===============================
email_input = wait.until(
    EC.presence_of_element_located((By.NAME, "username"))
)
email_input.send_keys(EMAIL)
email_input.send_keys(Keys.ENTER)
print("Email entered")

# ===============================
# 3️⃣ OTP INPUT (manual)
# ===============================
otp_input = wait.until(
    EC.presence_of_element_located((
        By.XPATH,
        "//input[@maxlength='6']"
    ))
)

print("👉 OTP manually enter karo (30 sec)")
time.sleep(30)  # yahan manually OTP dalo

print("✅ Login successful")

# ===============================
# Ab yahan cookies save kar sakte ho
# ===============================
