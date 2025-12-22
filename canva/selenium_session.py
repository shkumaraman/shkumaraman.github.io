import pickle, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

TARGET_URL = "https://www.canva.com/"

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
driver.get(TARGET_URL)

with open("cookies.pkl", "rb") as f:
    cookies = pickle.load(f)

for c in cookies:
    driver.add_cookie(c)

driver.refresh()
print("✅ Logged in session ready")

def get_page_source():
    return driver.page_source

def keep_alive():
    while True:
        time.sleep(300)
        driver.refresh()
