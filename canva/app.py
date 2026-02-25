from flask import Flask, make_response, redirect
import os

app = Flask(__name__)

# ================== YOUR FULL COOKIES ==================
YOUR_COOKIES = {
    'CL': 'en-IN',
    'ASI': '01KJBA1RJGZ1JF96FAD5ANWEJT',
    'FPLC': 'cwN7a%2FOD5xvJhhox8%2F0qxqhg6bFAWFtUE7gmmBij2VN9Q%2BRCNC7QgfMv7EU%2FUY2UkQYhS9VxIphagUEgqrh%2BaO5cQydyOBrcd%2FTuMIWHnDTY7PAwwdqEscXcIL5UhQ%3D%3D',
    'gtm_custom_user_engagement_lock_4': 'yes',
    '_ga': 'GA1.1.633366.1772053654',
    '_fbp': 'fb.1.1772053653819.648187711697904676',
    'FPAU': '1.2.1066189869.1772053654',
    'ab.storage.userId.320f7332-8571-45d7-b342-c54192dae547': 'g%3AUAEQadH2Jjk%7Ce%3Aundefined%7Cc%3A1772053658342%7Cl%3A1772053658352',
    'ab.storage.deviceId.320f7332-8571-45d7-b342-c54192dae547': 'g%3Abff99a8f-c2de-40a8-a6ad-c9d67f6d1a93%7Ce%3Aundefined%7Cc%3A1772053658356%7Cl%3A1772053658356',
    'gtm_custom_user_engagement': '{"lock":"yes","page":2,"landingPageURL":"https://www.canva.com/create-new","newSession":"no"}',
    'gtm_fpc_engagement_event': '{"url":"https://www.canva.com/create-new","ts":1772054283559,"utm_s":-1,"utm_m":-1}',
    '_uetsid': '01ee63e0128e11f1ad23614df1dc93c3',
    '_uetvid': '01eebb30128e11f19af3911e6aaf3b88',
    '_ga_EPWEMH6717': 'GS2.1.s1772053653$o1$g1$t1772054284$j57$l0$h2109609942$dW0oPzEoDrZivRfvodtCoAaga00hZLi79Ew',
    'ab.storage.sessionId.320f7332-8571-45d7-b342-c54192dae547': 'g%3Ab389319c-a1d7-454d-a93b-37aa447c15a9%7Ce%3A1772056088427%7Cc%3A1772053658349%7Cl%3A1772054288427'
}

@app.route('/')
def home():
    # Step 1: Redirect to Canva
    response = make_response(redirect("https://www.canva.com"))
    
    # Step 2: Attach all cookies
    for name, value in YOUR_COOKIES.items():
        response.set_cookie(
            key=name,
            value=value,
            domain='.canva.com',        # Important!
            path='/',
            secure=True,
            httponly=False,
            samesite='None'
        )
    
    return response

@app.route('/health')
def health():
    return {'status': 'alive', 'cookies_loaded': len(YOUR_COOKIES)}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
