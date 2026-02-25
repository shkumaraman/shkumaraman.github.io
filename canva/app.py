from flask import Flask, Response, request
import requests
import os
import brotli
import gzip
import zlib

app = Flask(__name__)

# ================== YOUR COOKIES (FULL) ==================
YOUR_COOKIES = {
    'CL': 'en-IN',
    'ASI': '01KJBA1RJGZ1JF96FAD5ANWEJT',
    'FPLC': 'cwN7a%2FOD5xvJhhox8%2F0qxqhg6bFAWFtUE7gmmBij2VN9Q%2BRCNC7QgfMv7EU%2FUY2UkQYhS9VxIphagUEgqrh%2BaO5cQydyOBrcd%2FTuMIWHnDTY7PAwwdqEscXcIL5UhQ%3D%3D',
    '_ga': 'GA1.1.633366.1772053654',
    '_fbp': 'fb.1.1772053653819.648187711697904676',
    '__cuid': 'f38ebcf18c514e9c884944e76e591278',
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    # Important: Accept encoding handle karenge
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}

def decode_content(response):
    """Response content ko decode karo based on encoding"""
    
    content_encoding = response.headers.get('Content-Encoding', '')
    content = response.content
    
    try:
        if 'br' in content_encoding:
            print("📦 Decoding Brotli...")
            content = brotli.decompress(content)
        elif 'gzip' in content_encoding:
            print("📦 Decoding Gzip...")
            content = gzip.decompress(content)
        elif 'deflate' in content_encoding:
            print("📦 Decoding Deflate...")
            content = zlib.decompress(content)
    except Exception as e:
        print(f"❌ Decode error: {e}")
    
    return content

@app.route('/')
@app.route('/<path:path>')
def proxy(path=''):
    # Target URL
    if path:
        target_url = f'https://www.canva.com/{path}'
    else:
        target_url = 'https://www.canva.com'
    
    print(f"🌐 Fetching: {target_url}")
    
    # Session with cookies
    session = requests.Session()
    session.cookies.update(YOUR_COOKIES)
    session.headers.update(HEADERS)
    
    try:
        # Forward query parameters
        if request.query_string:
            target_url += f'?{request.query_string.decode()}'
        
        # Make request
        resp = session.get(target_url, timeout=15, stream=True)
        print(f"📥 Response Status: {resp.status_code}")
        print(f"📥 Content-Type: {resp.headers.get('content-type', 'unknown')}")
        print(f"📥 Content-Encoding: {resp.headers.get('content-encoding', 'none')}")
        
        # Decode content if compressed
        content = decode_content(resp)
        
        # Agar HTML hai toh text mein convert karo
        if 'text/html' in resp.headers.get('content-type', ''):
            try:
                content = content.decode('utf-8')
            except:
                try:
                    content = content.decode('latin-1')
                except:
                    pass
        
        # Create response with decoded content
        response = Response(
            content,
            status=resp.status_code,
            content_type=resp.headers.get('content-type', 'text/html')
        )
        
        # Remove content-encoding header kyunki hum decode kar chuke
        response.headers.pop('Content-Encoding', None)
        
        return response
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return f"""
        <html>
        <body style="font-family: Arial; padding: 20px;">
            <h2>Error Loading Canva</h2>
            <p>{str(e)}</p>
            <button onclick="location.reload()">⟳ Try Again</button>
        </body>
        </html>
        """, 500

@app.route('/health')
def health():
    return {'status': 'alive'}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
