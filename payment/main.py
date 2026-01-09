from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import razorpay
import os
import hmac, hashlib

app = FastAPI()

# CORS (Universal Frontend Support)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Razorpay Client
client = razorpay.Client(
    auth=(
        os.getenv("RAZORPAY_KEY_ID"),
        os.getenv("RAZORPAY_KEY_SECRET")
    )
)

# Health Check
@app.get("/")
def health():
    return {"status": "ok"}

# 1️⃣ Create Order
@app.post("/create-order")
async def create_order(request: Request):
    data = await request.json()
    amount = data.get("amount")

    if not amount or float(amount) <= 0:
        raise HTTPException(status_code=400, detail="Valid amount required")

    order = client.order.create({
        "amount": int(float(amount) * 100),  # rupees → paise
        "currency": "INR",
        "payment_capture": 1
    })

    return {
        "order_id": order["id"],
        "amount": order["amount"],
        "currency": order["currency"],
        "key": os.getenv("RAZORPAY_KEY_ID")
    }

# 2️⃣ Verify Payment (Frontend triggered)
@app.post("/verify-payment")
async def verify_payment(request: Request):
    data = await request.json()

    try:
        client.utility.verify_payment_signature({
            "razorpay_order_id": data["razorpay_order_id"],
            "razorpay_payment_id": data["razorpay_payment_id"],
            "razorpay_signature": data["razorpay_signature"]
        })
        return {"status": "success"}
    except:
        raise HTTPException(status_code=400, detail="Payment verification failed")

# 3️⃣ Webhook (Razorpay server-to-server)
@app.post("/razorpay-webhook")
async def razorpay_webhook(request: Request):
    webhook_secret = os.getenv("RAZORPAY_WEBHOOK_SECRET")  # Razorpay Dashboard me generate karke add karo
    body = await request.body()
    signature = request.headers.get("X-Razorpay-Signature")

    # Verify signature
    expected_signature = hmac.new(
        webhook_secret.encode(),
        body,
        hashlib.sha256
    ).hexdigest()

    if signature != expected_signature:
        return JSONResponse({"status": "invalid signature"}, status_code=400)

    payload = await request.json()
    event = payload.get("event")
    data = payload.get("payload")

    # Example: Payment captured
    if event == "payment.captured":
        payment_id = data["payment"]["entity"]["id"]
        order_id = data["payment"]["entity"]["order_id"]
        amount = data["payment"]["entity"]["amount"]
        print(f"[Webhook] Payment captured: Payment ID: {payment_id}, Order ID: {order_id}, Amount: {amount}")

        # Example:
        # db.update_payment(order_id=order_id, payment_id=payment_id, status="captured")

    return {"status": "ok"}
