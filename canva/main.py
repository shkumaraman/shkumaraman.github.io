import pickle
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

TARGET_URL = "https://www.canva.com/en_in/login/"

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
driver.get(TARGET_URL)

# Load cookies
with open("cookies.pkl", "rb") as f:
    cookies = pickle.load(f)

for cookie in cookies:
    driver.add_cookie(cookie)

driver.refresh()
print("✅ Logged in using cookies")

# Keep session alive
while True:
    time.sleep(300)
    driver.refresh()
    print("🔄 Session refreshed")
