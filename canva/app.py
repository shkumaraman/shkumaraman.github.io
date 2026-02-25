import requests
from flask import Flask, Response
import os
import random

app = Flask(__name__)

COOKIES = {
    'ASI': '01KJBA1RJGZ1JF96FAD5ANWEJT',
    'CL': 'en-IN',
    'FPLC': 'cwN7a%2FOD5xvJhhox8%2F0qxqhg6bFAWFtUE7gmmBij2VN9Q%2BRCNC7QgfMv7EU%2FUY2UkQYhS9VxIphagUEgqrh%2BaO5cQydyOBrcd%2FTuMIWHnDTY7PAwwdqEscXcIL5UhQ%3D%3D'
}

PROXY_SOURCES = [
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt"
]

def get_working_proxy():
    """Multiple sources se proxy dhundo"""
    
    for source in PROXY_SOURCES:
        try:
            r = requests.get(source, timeout=5)
            proxies = r.text.strip().split('\n')[:20]
            
            for proxy in proxies:
                proxy = proxy.strip()
                if not proxy:
                    continue
                    
                proxy_url = f"http://{proxy}"
                
                # Test proxy
                try:
                    test = requests.get(
                        'http://httpbin.org/ip', 
                        proxies={'http': proxy_url, 'https': proxy_url},
                        timeout=3
                    )
                    if test.status_code == 200:
                        print(f"✅ Found: {proxy}")
                        return proxy_url
                except:
                    continue
        except:
            continue
    
    return None

@app.route('/')
@app.route('/<path:path>')
def proxy(path=''):
    """Main proxy handler"""
    
    target = f'https://www.canva.com/{path}' if path else 'https://www.canva.com'
    
    # Proxy dhundo
    proxy = get_working_proxy()
    if not proxy:
        return "No proxy available. Refresh to try again.", 503
    
    # Headers
    headers = {
        'User-Agent': random.choice([
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        ])
    }
    
    try:
        # Request with proxy
        session = requests.Session()
        session.proxies = {'http': proxy, 'https': proxy}
        session.cookies.update(COOKIES)
        session.headers.update(headers)
        
        resp = session.get(target, timeout=10)
        
        # Return response
        return Response(
            resp.text,
            status=resp.status_code,
            content_type=resp.headers.get('content-type', 'text/html')
        )
        
    except Exception as e:
        return f"Proxy error: {str(e)}. Refresh to try again.", 500

@app.route('/health')
def health():
    return {"status": "ok"}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
