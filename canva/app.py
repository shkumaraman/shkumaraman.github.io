import requests
import json
import random
import time
import os
from datetime import datetime

# Your cookies
COOKIES = {
    'ASI': '01KJBA1RJGZ1JF96FAD5ANWEJT',
    'CL': 'en-IN',
    'FPLC': 'cwN7a%2FOD5xvJhhox8%2F0qxqhg6bFAWFtUE7gmmBij2VN9Q%2BRCNC7QgfMv7EU%2FUY2UkQYhS9VxIphagUEgqrh%2BaO5cQydyOBrcd%2FTuMIWHnDTY7PAwwdqEscXcIL5UhQ%3D%3D',
    '_ga': 'GA1.1.633366.1772053654',
    '_fbp': 'fb.1.1772053653819.648187711697904676'
}

def get_proxy():
    """Fetch free proxy from Proxifly"""
    try:
        url = "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/https/data.json"
        response = requests.get(url, timeout=10)
        proxies = response.json()
        
        if proxies:
            proxy = random.choice(proxies[:30])
            proxy_url = f"http://{proxy['ip']}:{proxy['port']}"
            return proxy_url, proxy.get('country', 'Unknown')
    except:
        pass
    return None, None

def test_canva_with_proxy(proxy_url):
    """Test if proxy works with Canva"""
    session = requests.Session()
    session.proxies = {'http': proxy_url, 'https': proxy_url}
    session.cookies.update(COOKIES)
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    try:
        response = session.get('https://www.canva.com', timeout=15)
        return response.status_code == 200 and 'login' not in response.url.lower()
    except:
        return False

def main():
    print(f"🚀 Starting Canva Proxy Bot at {datetime.now()}")
    print("=" * 50)
    
    # Fetch proxy
    proxy_url, country = get_proxy()
    if not proxy_url:
        print("❌ No proxy found")
        return
    
    print(f"📡 Testing proxy: {proxy_url} [{country}]")
    
    # Test with Canva
    if test_canva_with_proxy(proxy_url):
        print("✅ SUCCESS! Canva accessible with proxy")
    else:
        print("❌ FAILED! Proxy not working with Canva")
    
    # Render health check ke liye
    print("\n✅ Bot executed successfully")

if __name__ == "__main__":
    main()
    
    # Render pe keep-alive ke liye (optional)
    # while True:
    #     time.sleep(300)  # 5 minutes
    #     main()
