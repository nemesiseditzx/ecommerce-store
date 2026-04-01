from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import stripe

app = FastAPI()

# ✅ STRIPE KEY (REPLACE THIS)
stripe.api_key = "YOUR_STRIPE_SECRET_KEY"

# ✅ CORS (allow frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# BASIC ROUTES
# -------------------------------

@app.get("/")
def home():
    return {"message": "Ecommerce API running 🚀"}

@app.get("/products")
def get_products():
    return [
        {"id": 1, "name": "Perfume A", "price": 50},
        {"id": 2, "name": "Perfume B", "price": 70},
        {"id": 3, "name": "Perfume C", "price": 90}
    ]

# -------------------------------
# ORDER SYSTEM (TEMP STORAGE)
# -------------------------------

orders = []

@app.post("/orders")
def create_order(order: dict):
    order_id = len(orders) + 1
    order["id"] = order_id
    order["order_status"] = "pending"

    orders.append(order)

    return {"order_id": order_id}

@app.get("/orders/{id}")
def get_order(id: int):
    for o in orders:
        if o["id"] == id:
            return o
    return {"error": "Not found"}

# -------------------------------
# STRIPE PAYMENT
# -------------------------------

@app.post("/create-checkout-session")
def create_checkout(order: dict):

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": "Order Payment",
                    },
                    "unit_amount": int(order["total"] * 100),
                },
                "quantity": 1,
            }
        ],
        mode="payment",

        # ✅ CHANGE THIS TO YOUR VERCEL URL
        success_url="https://ecommerce-store-coral-alpha.vercel.app/track.html",
        cancel_url="https://ecommerce-store-coral-alpha.vercel.app/",
    )

    return {"url": session.url}

# -------------------------------
# EMAIL (SIMULATION)
# -------------------------------

def send_email(to, subject, message):
    print(f"Email sent to {to}: {subject}")
