from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    page.goto("https://web.snapchat.com")
    input("Login manually and press Enter...")

    cookies = context.cookies()
    with open("cookies.json", "w") as f:
        json.dump(cookies, f)

    browser.close()
  
