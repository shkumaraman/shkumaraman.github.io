from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import razorpay
import os

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

# Health Check (Render needs this)
@app.get("/")
def health():
    return {"status": "ok"}

# 1️⃣ Create Order
@app.post("/create-order")
async def create_order(request: Request):
    data = await request.json()
    amount = data.get("amount")

    if not amount:
        raise HTTPException(status_code=400, detail="Amount required")

    order = client.order.create({
        "amount": int(amount) * 100,  # rupees → paise
        "currency": "INR",
        "payment_capture": 1
    })

    return {
        "order_id": order["id"],
        "amount": order["amount"],
        "currency": order["currency"],
        "key": os.getenv("RAZORPAY_KEY_ID")
    }

# 2️⃣ Verify Payment
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
