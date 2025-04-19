from playwright.sync_api import sync_playwright
import json
import time
import random

PROMO_LINK = "https://yourapp.link"  # <-- Replace this with your app link
MESSAGE_TEXT = f"Hey! Check this out: {PROMO_LINK}"

def send_message(page, friend, message):
    try:
        page.click('text=Chat')
        time.sleep(2)
        page.fill('input[placeholder="Search"]', friend)
        time.sleep(2)
        page.keyboard.press("Enter")
        time.sleep(3)
        page.fill('textarea', message)
        time.sleep(1)
        page.keyboard.press("Enter")
        print(f"Sent to {friend}")
    except Exception as e:
        print(f"Failed for {friend}: {e}")

def get_friends(page):
    """ Automatically fetch the friends list from Snapchat Web """
    page.click('text=Chat')  # Click on the Chat tab
    time.sleep(3)
    
    # We will try to extract all friends from the chat list
    friends_list = []
    
    # Scroll and fetch friend names
    for _ in range(10):  # Adjust the range to scroll more
        page.mouse.wheel(0, 1000)  # Scroll down
        time.sleep(1)
        friends = page.query_selector_all('div[role="listitem"] div[role="link"]')
        
        for friend in friends:
            name = friend.inner_text().strip()
            if name:
                friends_list.append(name)

    return friends_list

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()

    # Load cookies
    with open("cookies.json", "r") as f:
        cookies = json.load(f)
    context.add_cookies(cookies)

    page = context.new_page()
    page.goto("https://web.snapchat.com")
    time.sleep(5)

    # Get the list of friends automatically
    friends_list = get_friends(page)
    print(f"Found {len(friends_list)} friends.")

    # Send message to each friend
    for friend in friends_list:
        send_message(page, friend, MESSAGE_TEXT)
        time.sleep(random.uniform(4, 8))  # Random delay between messages

    browser.close()
