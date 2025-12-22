import pickle
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LOGIN_URL = "https://www.canva.com/en_in/login/"
EMAIL = "kumarsharma2580@gmail.com"

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 30)

driver.get(LOGIN_URL)

# Click continue button
wait.until(EC.element_to_be_clickable((
    By.XPATH, "//button[.//p[contains(text(),'Continue')]]"
))).click()

# Enter email
email_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
email_input.send_keys(EMAIL)
email_input.send_keys(Keys.ENTER)

print("👉 OTP manually enter karo (30 sec)")
time.sleep(30)

# Save cookies
with open("cookies.pkl", "wb") as f:
    pickle.dump(driver.get_cookies(), f)

print("✅ Cookies saved")
driver.quit()
