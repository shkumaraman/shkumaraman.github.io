from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import razorpay
import os
import hmac, hashlib

app = FastAPI()

# CORS
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
        "amount": int(float(amount) * 100),
        "currency": "INR",
        "payment_capture": 1
    })

    return {
        "order_id": order["id"],
        "amount": order["amount"],
        "currency": order["currency"],
        "key": os.getenv("RAZORPAY_KEY_ID")
    }

# 2️⃣ Verify Payment (Frontend)
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

# 3️⃣ Webhook (FIXED)
@app.post("/razorpay-webhook")
async def razorpay_webhook(request: Request):
    webhook_secret = os.getenv("RAZORPAY_WEBHOOK_SECRET")
    body = await request.body()
    signature = request.headers.get("X-Razorpay-Signature")

    # 🧪 Browser / Test call (NO signature)
    if not signature:
        return JSONResponse(
            {
                "status": "ok",
                "message": "Webhook received (browser/test call – no signature)"
            },
            status_code=200
        )

    # 🔐 Real Razorpay verification
    expected_signature = hmac.new(
        webhook_secret.encode(),
        body,
        hashlib.sha256
    ).hexdigest()

    if signature != expected_signature:
        return JSONResponse(
            {"status": "invalid signature"},
            status_code=400
        )

    payload = await request.json()
    event = payload.get("event")
    data = payload.get("payload")

    if event == "payment.captured":
        payment = data["payment"]["entity"]
        print(
            f"[Webhook] Payment captured | "
            f"payment_id={payment['id']} | "
            f"order_id={payment['order_id']} | "
            f"amount={payment['amount']}"
        )

    return {"status": "ok", "event": event}
